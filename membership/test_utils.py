# -*- coding: utf-8 -*-
import logging
from random import Random

# Use predictable random for consistent tests
random = Random()
random.seed(1)

logger = logging.getLogger("membership.test_utils")

from membership.models import Membership, Contact


# We use realistic names in test data so that it is feasible to test
# duplicate member detection code locally without using production data.

# Finnish population register center's most popular first names for year 2009
first_names = [
    "Maria", "Juhani", "Aino", "Veeti", "Emilia", "Johannes", "Venla",
    "Eetu", "Sofia", "Mikael", "Emma", "Onni", "Olivia", "Matias",
    "Ella", "Aleksi", "Aino", "Olavi", "Sofia", "Leevi", "Amanda",
    "Onni", "Aada", "Elias", "Matilda", "Ilmari", "Sara", "Lauri",
    "Helmi", "Oskari", "Iida", "Joona", "Aurora", "Elias", "Anni",
    "Matias", "Ilona", "Oliver", "Helmi", "Leo", "Iida", "Eemeli",
    "Emilia", "Niilo", "Eveliina", "Valtteri", "Siiri", "Rasmus", "Katariina",
    "Aleksi", "Veera", "Oliver", "Ella", "Antero", "Sanni", "Miro",
    "Aada", "Viljami", "Vilma", "Jimi", "Kristiina", "Kristian", "Nea",
    "Aatu", "Anni", "Tapani", "Milla", "Daniel", "Johanna", "Samuel",
    "Pinja", "Juho", "Emma", "Lauri", "Lotta", "Aapo", "Sara",
    "Tapio", "Olivia", "Eemeli", "Linnea", "Veeti", "Elli", "Jesse",
    "Anna", "Eetu", "Emmi", "Arttu", "Elina", "Emil", "Ronja",
    "Lenni", "Venla", "Petteri", "Elsa", "Valtteri", "Julia", "Daniel",
    "Nella", "Otto", "Aleksandra", "Eemil", "Kerttu", "Aaro", "Helena",
    "Juho", "Oona", "Joel", "Siiri", "Leevi", "Viivi", "Niklas",
    "Karoliina", "Joona", "Julia", "Ville", "Inkeri", "Julius", "Pihla",
    "Roope", "Alexandra", "Elmeri", "Peppi", "Konsta", "Alisa", "Leo",
    "Nelli", "Juuso", "Susanna", "Otto", "Neea", "Luka", "Josefiina",
    "Aleksanteri", "Jenna", "Mikael", "Kaarina", "Akseli", "Laura", "Samuel",
    "Lotta", "Sakari", "Anna", "Oskari", "Alina", "Anton", "Milja",
    "Julius", "Ellen", "Veikko", "Enni", "Luukas", "Veera", "Toivo",
    "Alisa", "Jere", "Sanni", "Eino", "Ilona", "Niko", "Kerttu",
    "Niilo", "Inka", "Eelis", "Elsa", "Jaakko", "Amanda", "Eeli",
    "Elli", "Rasmus", "Minea", "Anton", "Vilma", "Antti", "Matilda",
    "Eino", "Vilhelmiina", "V??in??", "Iina", "Emil", "Nea", "Henrik",
    "Eevi", "Kasper", "Anneli", "Matti", "Ellen", "Tuomas", "Maija",
    "Aatu", "Saana", "Eemil", "Tuulia", "Kalevi", "Minttu", "Akseli",
    "Anniina", "Joonatan", "Lilja", "Viljami"]

# Kapsi members public unique last name listing as of today.
last_names = [
    "Aalto", "Aaltonen", "Addams-Moring", "Aho", "Ahola", "Ahonen",
    "Aimonen", "Al-Khanji", "Ala-Kojola", "Alakotila", "Alanenp????", "Alanko",
    "Alardt", "Alasp????", "Alatalo", "Andelin", "Annala", "Antinkaapo",
    "Anttila", "Anttonen", "Arstila", "Arvelin", "Auvinen", "Averio",
    "Bainton", "Behm", "Blomberg", "Bor??n", "Brander", "Brockman",
    "Brunberg", "Busk", "Ceder", "Corsini", "Duldin", "Eerik??inen",
    "Eerola", "Ekblom", "Ekman", "Eloranta", "Emas", "Eriksson",
    "Ernsten", "Erola", "Er??luoto", "Eskelinen", "Eskola", "Everil??",
    "Finnil??", "Fj??llstr??m", "Forslund", "Grandell", "Grenrus", "Gr??hn",
    "Gr??nlund", "Haapaj??rvi", "Haapala", "Haasanen", "Haatainen", "Haataja",
    "Haavisto", "Hagelberg", "Hahtola", "Haikonen", "Haimi", "Hakanen",
    "Hakkarainen", "Halkosaari", "Halla", "Hallamaa", "Hallikainen", "Halme",
    "Halmu", "Halonen", "Hamara", "Hanhij??rvi", "Hannola", "Hannus",
    "Hansson", "Harju", "Harkila", "Harma", "Hasanen", "Hassinen",
    "Hast", "Hastrup", "Hatanp????", "Haverinen", "Heikker??", "Heikkil??",
    "Heikkinen", "Heikura", "Heimonen", "Heinikangas", "Heinonen", "Hein??nen",
    "Heiramo", "Heiskanen", "Helander", "Helenius", "Herd", "Herranen",
    "Herukka", "Heusala", "Hietala", "Hietanen", "Hietaranta", "Hiilesrinne",
    "Hiljander", "Hill", "Hillervo", "Hiltunen", "Hinkula", "Hintikka",
    "Hirvoj??rvi", "Holopainen", "Hongisto", "Honkanen", "Honkonen", "Hopiavuori",
    "Hotti", "Huhtala", "Huhtinen", "Hulkko", "Huoman", "Huotari",
    "Huovinen", "Hurtta", "Huttunen", "Huuhtanen", "Huuskonen", "Hyttinen",
    "Hyv??rinen", "H??kkinen", "H??meenkorpi", "H??m??l??inen", "H??nninen", "H??glund",
    "Ihatsu", "Ij??s", "Ikonen", "Ilmonen", "Iltanen", "Ingman",
    "Inha", "Inkinen", "Isaksson", "Isom??ki", "Ituarte", "It??salo",
    "Jaakkola", "Jaatinen", "Jakobsson", "Jalonen", "Jetsu", "Johansson",
    "Jokela", "Jokinen", "Jokitalo", "Jormanainen", "Junni", "Juopperi",
    "Juutinen", "Juvankoski", "Juvonen", "J??rvenp????", "J??rvensivu", "J??rvinen",
    "J????skel??", "J????skel??inen", "Kaarela", "Kaartti", "Kaija", "Kaikkonen",
    "Kaila", "Kainulainen", "Kajan", "Kakko", "Kallio", "Kanniainen",
    "Kanninen", "Kare-M??kiaho", "Karhunen", "Kari", "Karim??ki", "Karisalmi",
    "Karjalainen", "Karlsson", "Karppi", "Karttunen", "Karvinen", "Karvonen",
    "Kasari", "Kataja", "Katavisto", "Kattelus", "Kauppi", "Kauppinen",
    "Keih??nen", "Keijonen", "Kekki", "Kekkonen", "Kelanne", "Kentt??l??",
    "Ker??nen", "Keskitalo", "Kesti", "Ketolainen", "Ketonen", "Kettinen",
    "Kianto", "Kiiskil??", "Kilpi??inen", "Kinnula", "Kinnunen", "Kirkkopelto",
    "Kirves", "Kittil??", "Kiviharju", "Kivikunnas", "Kivilahti", "Kiviluoto",
    "Kivim??ki", "Kivirinta", "Knuutinen", "Kohtam??ki", "Kois", "Koivisto",
    "Koivu", "Koivula", "Koivulahti", "Koivumaa", "Koivunalho", "Koivunen",
    "Koivuranta", "Kokkonen", "Kokkoniemi", "Komulainen", "Konsala", "Konttila",
    "Konttinen", "Koponen", "Korhonen", "Kortesalmi", "Kortetm??ki", "Koskela",
    "Koskenniemi", "Koski", "Petteri", "Koskinen", "Kotanen", "Koulu",
    "Kraft", "Krohn", "Kr??ger", "Kudjoi", "Kuhanen", "Kuittinen",
    "Kuitunen", "Kujala", "Kujansuu", "Kulju", "Kurkim??ki", "Kuukasj??rvi",
    "Kuusisto", "Kuvaja", "Kym??l??inen", "Kynt??aho", "K??hk??nen", "K??ki",
    "K??rkk??inen", "K??rn??", "Laaksonen", "Laalo", "Laapotti", "Lagren",
    "Lagus", "Lahdenm??ki", "Lahdenper??", "Lahikainen", "Lahtela", "Laine",
    "Lainiola", "Laitila", "Laitinen", "Untamo", "Lakhan", "Lamminen",
    "Lammio", "Lampela", "Lamp??n", "Lampi", "Lampinen", "Lankila",
    "Lapinniemi", "Lappalainen", "Larivaara", "Larja", "Latvatalo", "Laurila",
    "Laxstr??m", "Lehmuskentt??", "Lehtinen", "Lehtola", "Lehtonen", "Leikkari",
    "Leivisk??", "Leivo", "Lempinen", "Lepist??", "Lepp??nen", "Levonen",
    "Lievemaa", "Liimatta", "Likitalo", "Liljeqvist", "Lindeman", "Lind??n",
    "Lindfors", "Lindstr??m", "Linkoaho", "Linkola", "Linnaluoto", "Linnam??ki",
    "Lintervo", "Lintum??ki", "Lipsanen", "Liukkonen", "Loikkanen", "Loponen",
    "Louhiranta", "Lundan", "Luosmaa", "Luukko", "Luukkonen", "L??hdem??ki",
    "L??hteenm??ki", "L??fgren", "L??ytty", "Maaranen", "Magga", "Makkonen",
    "Maksimainen", "Malinen", "Malm", "Malmivirta", "Manner", "Manninen",
    "Mansikkala", "Marin", "Marjamaa", "Marjoneva", "Markkanen", "Martikainen",
    "Marttila", "Matikainen", "Matkaselk??", "Mattila", "Maukonen", "Melama",
    "Melenius", "Mellin", "Merikivi", "Meril??inen", "Merisalo", "Meskanen",
    "Miettunen", "Miinin", "Mikkonen", "Moisala", "Moisio", "Mononen",
    "Montonen", "Mustonen", "Myllym??ki", "Myllyselk??", "Myntti", "Myyry",
    "M??h??nen", "M??kel??", "M??kel??inen", "M??kinen", "M??kitalo", "M??nki",
    "M??ntyl??", "M??rsy", "M??tt??", "M??yr??nen", "M????tt??", "M??ller",
    "Nemeth", "Niemel??", "Niemenmaa", "Niemi", "Nieminen", "Niiranen",
    "Nikander", "Nikkonen", "Nikula", "Niskanen", "Nisula", "Nousiainen",
    "Nummiaho", "Nurmi", "Nurminen", "Nygren", "Nyk??nen", "Nylund",
    "Nyrhil??", "N??yh??", "Ohtamaa", "Ojala", "Ollila", "Olmari",
    "Oras", "Paajanen", "Paalanen", "Paananen", "Packalen", "Pahalahti",
    "Paimen", "Pakkanen", "Palo", "Palokangas", "Palom??ki", "Palosaari",
    "Panula", "Pappinen", "Parkkinen", "Partanen", "Parviainen", "Pasila",
    "Paul", "Pekkanen", "Peltola", "Peltonen", "Pennala", "Pentik??inen",
    "Penttil??", "Perttunen", "Per??l??", "Pesonen", "Peuhkuri", "Peurakoski",
    "Piesala", "Pietarinen", "Pietik??inen", "Pietil??", "Pievil??inen", "Pihkala",
    "Pihlaja", "Pihlajaniemi", "Piittinen", "Pikkarainen", "Pirinen", "Pirttij??rvi",
    "Pitk??nen", "Pohjalainen", "Pohjanraito", "Pohjola", "Pokkinen", "Polso",
    "Portaankorva", "Portti", "Posti", "Prusi", "Pulliainen", "Puranen",
    "Pusa", "Pussinen", "Pyh??j??rvi", "Pylv??n??inen", "P??l??nen", "P??ykk??",
    "Raatikainen", "Rahikainen", "Rainela", "Raitanen", "Raitmaa", "Raittila",
    "Rajala", "Rajam??ki", "Ranki", "Ranta", "Rantala", "Rantam??ki",
    "Rapo", "Rasilainen", "Rauhala", "Rautiainen", "Rehu", "Reijonen",
    "Reunanen", "Riikonen", "Rimpil??inen", "Rissanen", "Ristil??", "Rokka",
    "Roponen", "Ruhanen", "Runonen", "Rutanen", "Ruuhonen", "Ruusu",
    "Ryh??nen", "Rytk??nen", "R??s??nen", "R??ty", "R??nkk??", "R??ssi",
    "Saarenm??ki", "Saarijoki", "Saarikoski", "Saarinen", "Saastamoinen", "Saine",
    "Saksa", "Salkia", "Salmela", "Salmi", "Salminen", "Salo",
    "Salokanto", "Salomaa", "Salom??ki", "Salonen", "Sand", "Sanisalo",
    "Santala", "Savolainen", "Schwartz", "Selin", "Sepp??", "Sepp??l??",
    "Sepp??nen", "Set??l??", "Siekkinen", "Siev??nen", "Sihvo", "Siironen",
    "Siitonen", "Silfver", "Sillanp????", "Siltala", "Simola", "Simon",
    "Siniluoto", "Sinivaara", "Sipil??", "Sivula", "Sj??berg", "Soili",
    "Soini", "Soininen", "Solja", "Solkio", "Sonck", "Sopanen",
    "Sotejeff", "Staven", "Strand", "Suckman", "Sunell", "Suolahti",
    "Suominen", "Suoniitty", "Suonvieri", "Suorsa", "Suvanne", "Syreeni",
    "Syrj??", "Syrj??l??", "Syv??nen", "S??rkk??", "S????m??ki", "S????skilahti",
    "S??dervall", "Tahvanainen", "Taina", "Taipale", "Taivalsalmi", "Tallqvist",
    "Tamminen", "Tammisto", "Tanhua", "Tanner", "Tanskanen", "Tapper-Veirto",
    "Tarsa", "Tarvainen", "Tiainen", "Tiira", "Tikka", "Tikkanen",
    "Toivanen", "Toivonen", "Tolvanen", "Tulonen", "Tunkkari", "Tuohimaa",
    "Tuomela", "Tuomi", "Tuomimaa", "Tuominen", "Tuomivaara", "Turanlahti",
    "Turpeinen", "Turunen", "Tuunainen", "Tuusa", "Tykk??", "Tyrv??inen",
    "T??htinen", "T??tt??", "Urhonen", "Uuksulainen", "Uusitalo", "Vaarala",
    "Vaaramaa", "Vainio", "Vainionp????", "Valkeinen", "Valkonen", "Valtonen",
    "Valve", "Varanka", "Varrio", "Varsaluoma", "Vartiainen", "Veijalainen",
    "Veijola", "Velhonoja", "Ven??l??inen", "Vesala", "Vesiluoma", "Vestu",
    "Vierimaa", "Viippola", "Viitala", "Viitanen", "Vilkki", "Vilppunen",
    "Vire", "Virta", "Virtala", "Virtanen", "Vitikka", "Voipio",
    "Vuokko", "Vuola", "Vuollet", "Vuorela", "Vuorinen", "V??h??kyl??",
    "V??h??m??ki", "V??h??nen", "V??is??nen", "V??limaa", "V????n??nen", "Wahalahti",
    "Wikman", "Yli-Hukka", "Ylim??inen", "Ylinen", "Yl??nen", "Yrttikoski",
    "??ij??nen", "??rm??nen"]


def random_first_name():
    return random.choice(first_names)


def random_last_name():
    return random.choice(last_names)


def create_dummy_member(status, type='P', mid=None):
    if status not in ['N', 'P', 'A']:
        raise Exception("Unknown membership status")  # pragma: no cover
    if type not in ['P', 'S', 'O', 'H']:
        raise Exception("Unknown membership type")  # pragma: no cover
    i = random.randint(1, 300)
    fname = random_first_name()
    d = {
        'street_address' : 'Testikatu %d'%i,
        'postal_code' : '%d' % (i+1000),
        'post_office' : 'Paska kaupunni',
        'country' : 'Finland',
        'phone' : "%09d" % (40123000 + i),
        'sms' : "%09d" % (40123000 + i),
        'email' : 'user%d@example.com' % i,
        'homepage' : 'http://www.example.com/%d'%i,
        'first_name' : fname,
        'given_names' : '%s %s' % (fname, "Kapsi"),
        'last_name' : random_last_name(),
    }
    contact = Contact(**d)
    contact.save()
    if type in ('O', 'S'):
        contact.organization_name = contact.name()
        contact.first_name = ''
        contact.last_name = ''
        contact.save()
        membership = Membership(id=mid, type=type, status=status,
                                organization=contact,
                                nationality='Finnish',
                                municipality='Paska kaupunni',
                                extra_info='Hintsunlaisesti semmoisia tietoja.')
    else:
        membership = Membership(id=mid, type=type, status=status,
                                person=contact,
                                nationality='Finnish',
                                municipality='Paska kaupunni',
                                extra_info='Hintsunlaisesti semmoisia tietoja.')
    logger.info("New application %s from %s:." % (str(contact), '::1'))
    membership.save()
    return membership


class MockLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected logs as per:
    <http://stackoverflow.com/questions/899067/how-should-i-verify-a-log-message-when-testing-python-code-under-nose/1049375#1049375>"""
    def __init__(self, *args, **kwargs):
        self.reset()
        logging.Handler.__init__(self, *args, **kwargs)

    def emit(self, record):
        self.messages[record.levelname.lower()].append(record.getMessage())

    def reset(self):
        self.messages = {
            'debug': [],
            'info': [],
            'warning': [],
            'error': [],
            'critical': [],
        }
