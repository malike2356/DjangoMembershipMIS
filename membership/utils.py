# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

from membership.models import BillingCycle, Bill, Contact, Membership

# http://code.activestate.com/recipes/576644/

def dict_diff(first, second):
    """ Return a dict of keys that differ with another config object.  If a value is
        not found in one fo the configs, it will be represented by KEYNOTFOUND.
        @param first:   Fist dictionary to diff.
        @param second:  Second dicationary to diff.
        @return diff:   Dict of Key => (first.val, second.val)
    """
    diff = {}
    sd1 = set(first)
    sd2 = set(second)
    #Keys missing in the second dict
    for key in sd1.difference(sd2):
        diff[key] = (first[key], None)
    #Keys missing in the first dict
    for key in sd2.difference(sd1):
        diff[key] = (None, second[key])
    #Check for differences
    for key in sd1.intersection(sd2):
        if first[key] != second[key]:
            diff[key] = (first[key], second[key])
    return diff

def diff_humanize(diff):
    # Human readable output
    txt = ""
    for key in diff:
        if key == 'last_changed' or key.startswith("_"):
            continue
        change = diff[key]
        if change[0] == None:
            txt += "%s: () -> '%s'. " % (key, change[1])
        elif change[1] == None:
            txt += "%s: '%s' -> (). " % (key, change[0])
        else:
            txt += "%s: '%s' => '%s'. " % (key, change[0], change[1])
    return txt
    
def new_cycle(membership):
    old_cycle = membership.billingcycle_set.order_by('-end')[0]
    billing_cycle = BillingCycle(membership=membership, start=old_cycle.end)
    billing_cycle.save() # Creating an instance does not touch db and we need and id for the Bill
    bill = Bill(cycle=billing_cycle)
    bill.save()
    bill.send_as_email()

def sendreminder(membership): # XXX Test if cycle is paid?
    billing_cycle = membership.billingcycle_set.order_by('-end')[0]
    bill = Bill(cycle=billing_cycle)
    bill.save()
    bill.send_as_email()

def disable_member(membership):
    pass # XXX

def log_change(object, user, before=None, after=None, change_message=None):
    if not change_message:
        if before and after:
            change_message  = diff_humanize(dict_diff(before, after))
        else:
            change_message = "Some changes were made"
    from django.contrib.admin.models import LogEntry, CHANGE
    LogEntry.objects.log_action(
        user_id         = user.pk,
        content_type_id = ContentType.objects.get_for_model(object).pk,
        object_id       = object.pk,
        object_repr     = force_unicode(object),
        action_flag     = CHANGE,
        change_message  = change_message
    )

def contact_from_dict(d):
    if d is None:
        return None
    
    try:
        c = Contact(street_address=d['street_address'],
                    postal_code=d['postal_code'],
                    post_office=d['post_office'],
                    country=d['country'],
                    phone=d['phone'],
                    sms=d['sms'],
                    email=d['email'],
                    homepage=d['homepage'])
    except:
        return None
    
    if d.has_key('organization_name') and len(d['organization_name']) > 5:
        c.organization_name = d['organization_name']
    else:
        c.first_name = d['first_name']
        c.given_names = d['given_names']
        c.last_name = d['last_name']
    return c

def serializable_membership_info(membership):
    """
    A naive method of dict construction is used here. It's not very fancy,
    but Django's serialization seems to take such a tedious route that this
    seems simpler.
    """
    json_obj = {}
    # Membership details
    for attr in ['type', 'status', 'created', 'last_changed', 'municipality',
                 'nationality', 'extra_info']:
        # Get the translated value for choice fields, not database field values
        if attr in ['type', 'status']:
            attr_val = getattr(membership, 'get_' + attr + '_display')()
        else:
            attr_val = getattr(membership, attr, u'')
        
        if isinstance(attr_val, basestring):
            json_obj[attr] = attr_val
        elif isinstance(attr_val, datetime):
            json_obj[attr] = attr_val.ctime()
        else:
            json_obj[attr] = unicode(attr_val)
    json_obj['str'] = unicode(membership)

    # Contacts
    contacts_json_obj = {}
    json_obj['contacts'] = contacts_json_obj
    for attr in ['person', 'billing_contact', 'tech_contact', 'organization']:
        attr_val = getattr(membership, attr, None)
        if not attr_val:
            continue

        contact_json_obj = {}
        for c_attr in ['first_name', 'given_names', 'last_name',
                       'organization_name', 'street_address', 'postal_code',
                       'post_office', 'country', 'phone', 'sms', 'email',
                       'homepage']:
            c_attr_val = getattr(attr_val, c_attr, u'')
            contact_json_obj[c_attr] = c_attr_val
            contacts_json_obj[attr] = contact_json_obj

    # Events (comments + log entries)
    comment_list = []
    log_entry_list = []
    event_list = []
    json_obj['comments'] = comment_list
    json_obj['log_entries'] = log_entry_list
    json_obj['events'] = event_list
    
    comments = Comment.objects.filter(object_pk=membership.pk)
    for comment in comments:
        d = { 'user_name': unicode(comment.user),
              'text': comment.comment,
              'date': comment.submit_date }
        comment_list.append(d)
        event_list.append(d)

    log_entries = membership.logs.all()
    for entry in log_entries:
        d = { 'user_name': unicode(entry.user),
              'text': "%s %s" % (unicode(entry.action_flag), unicode(entry.change_message)),
              'date': entry.action_time }
        log_entry_list.append(d)
        event_list.append(d)

    def cmp_fun(x, y):
        if x['date'] > y['date']:
            return 1
        if x['date'] == y['date']:
            return 0
        return -1

    comment_list.sort(cmp_fun)
    log_entry_list.sort(cmp_fun)
    event_list.sort(cmp_fun)

    def ctimeify(lst):
        for item in lst:
            if isinstance(item['date'], basestring):
                continue # some are already in ctime format since they are part of multiple lists
            item['date'] = item['date'].ctime()
    ctimeify(comment_list)
    ctimeify(log_entry_list)
    ctimeify(event_list)

    return json_obj

def _do_save_membership_status_change_comment(user, membership, comment_text):
    comment = Comment()
    comment.user = user
    comment.content_object = membership
    comment.comment = comment_text
    comment.site_id = settings.SITE_ID
    comment.submit_date = datetime.now()
    return comment.save()

def save_membership_approved_comment(user, membership):
    return _do_save_membership_status_change_comment(user, membership, u"Approved")

def save_membership_preapproved_comment(user, membership):
    return _do_save_membership_status_change_comment(user, membership, u"Preapproved")
