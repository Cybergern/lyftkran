import random
import unicodedata
from datetime import datetime
from random import randint

from ..models import (Club, Competition, CompetitionType, ContactInformation, District, GenderChoices, Invitation, 
                           License, LicenseStatus, Lifter, Result)

CITY_NAME_CHOICES = ("Stockholm", "Göteborg", "Malmö", "Uppsala", "Västerås", "Örebro", "Linköping",
                        "Helsingborg", "Jönköping", "Norrköping", "Lund", "Umeå", "Gävle", "Solna", "Växjö")
CLUB_SUFFIX_CHOICES = ("SK", "TK", "AK", "KK", "IK", "IF")
DISTRICTS = ("Mellersta Norrlands SDF", "Norra Norrlands SDF", "Sydsvenska SDF", "Sydöstra SDF", "Södra Norrlands SDF",
                "Västra Götalands SDF", "Västra Svealands SDF", "Östra Svealands SDF")
ROAD_BASE = ("Tiger", "Löv", "Folkunga", "Kungs", "Drottning",
                "Vikinga", "Gran", "Kyrko", "Katedral")
ROAD_SUFFIX = ("vägen", "gatan", "avenyn", "gränd")

with open('lifter/test/data/female_first_names.txt', 'r') as reader:
    FEMALE_FIRST_NAME_CHOICES = reader.read().splitlines()
with open('lifter/test/data/male_first_names.txt', 'r') as reader:
    MALE_FIRST_NAME_CHOICES = reader.read().splitlines()
with open('lifter/test/data/family_names.txt', 'r') as reader:
    LAST_NAME_CHOICES = reader.read().splitlines()

used_email_prefixes = []

def get_random_date() -> datetime.date:
    return datetime.strptime("%i-%i-%i" % (randint(1970, 2005), randint(1, 12), randint(1, 28)), "%Y-%m-%d")

def get_random_id() -> str:
    date = get_random_date()
    personal_number = date.strftime("%Y%m%d") + str(randint(100, 999))
    full_sum = 0
    for x in range(0, len(personal_number[2:])):
        prod = (2 - (x % 2)) * int(personal_number[2:][x])
        full_sum += sum([int(d) for d in str(prod)])
    control_number = (10 - (full_sum % 10)) % 10
    return personal_number + str(control_number)

def get_random_club_name_and_email() -> tuple[str, str]:
    club_name = random.choice(CITY_NAME_CHOICES) + " " + random.choice(CLUB_SUFFIX_CHOICES)
    club_email = club_name.lower().replace(" ", "_") + "@gmail.com"
    return club_name, club_email

def get_random_name_and_email(gender: GenderChoices) -> tuple[str, str, str]:
    if gender == GenderChoices.FEMALE:
        first_name = random.choice(FEMALE_FIRST_NAME_CHOICES)
    else:
        first_name = random.choice(MALE_FIRST_NAME_CHOICES)
    family_name = random.choice(LAST_NAME_CHOICES)
    email_prefix = unicodedata.normalize("NFKD", f"{first_name}.{family_name}".lower()).encode("ascii", "ignore").decode("ascii")
    email_prefix = get_unique_email_prefix(email_prefix, 0)
    return first_name, family_name, f"{email_prefix}@gmail.com"

def get_random_gender() -> GenderChoices:
    return random.choice(list(GenderChoices))

def get_unique_email_prefix(prefix: str, cur: int) -> str:
    test_prefix = f"{prefix}{cur if cur > 0 else ''}"
    if test_prefix not in used_email_prefixes:
        used_email_prefixes.append(test_prefix)
        return test_prefix
    else:
        return get_unique_email_prefix(prefix, cur + 1)


def get_random_address() -> str:
    return "%s%s %s" % (random.choice(ROAD_BASE), random.choice(ROAD_SUFFIX), str(randint(1, 99)))

def get_random_contact_info(email: str) -> ContactInformation:
    return ContactInformation.objects.create(address=get_random_address(), postal_code=get_random_postal_code(),
                                        postal_city=get_random_city(), phone=get_random_phone(),
                                        email=email)

def get_random_postal_code() -> int:
    return randint(10000, 99999)

def get_random_phone() -> str:
    return "070-" + str(randint(1000000, 9999999))

def get_random_city() -> str:
    return random.choice(CITY_NAME_CHOICES)

def create_all_districts() -> list[District]:
    for dis_name in DISTRICTS:
        dis_email = dis_name.lower().replace(" ", "_") + "@gmail.com"
        contact_info = get_random_contact_info(dis_email)
        District.objects.create(name=dis_name, contact_information=contact_info)
    return District.objects.all()

def create_club(district: District = None) -> Club:
    club_name, club_email = get_random_club_name_and_email()
    while club_name in [club.name for club in Club.objects.all()]:
        club_name, club_email = get_random_club_name_and_email()
    contact_info = get_random_contact_info(club_email)
    club_district = district if district else random.choice(District.objects.all())
    return Club.objects.create(name=club_name, district=club_district, contact_information=contact_info)

def create_lifter(clubs: list[Club]) -> Lifter:
    gender = get_random_gender()
    first_name, family_name, email = get_random_name_and_email(gender)
    contact_info = get_random_contact_info(email)
    lifter = Lifter.objects.create(first_name=first_name, family_name=family_name,
                                    contact_information=contact_info,
                                    gender=gender, id_number=get_random_id())
    lifter.clubs.set(clubs)
    create_licenses(lifter)
    return lifter

def get_random_club_list() -> list[Club]:
    no_of_clubs = random.randint(1, 3)
    return random.choices(Club.objects.all(), k=no_of_clubs)

def rand_boolean() -> bool:
    return bool(random.getrandbits(1))

def create_licenses(license_lifter: Lifter) -> list[License]:
    licenses = []
    year_now = int(datetime.now().strftime("%Y"))
    for x in range(year_now - 10, year_now + 1):
        if rand_boolean():
            license_number = license_lifter.id_number[2:8] + \
                                license_lifter.first_name[0].lower() + \
                                license_lifter.family_name[0].lower()
            license_year = x
            license_status = random.choice(list(LicenseStatus))
            licenses.append(License.objects.create(
                lifter=license_lifter, number=license_number, year=license_year, status=license_status,
                club=license_lifter.clubs.all()[0]))
    return licenses
            
def create_competition(club: Club, results: list[Result] = None) -> Competition:
    invitation = create_invitation(club)
    results = results if results else []
    competition = Competition.objects.create(invitation=invitation)
    competition.results.set(results)
    return competition


def create_invitation(club: Club) -> Invitation:
    name = "Competition by " + club.name
    competition_type = CompetitionType.objects.create(name="CP")
    invitation = Invitation.objects.create(
        name=name, description=name, organizer=club, start_date=get_random_date(), finish_date=get_random_date(), 
        last_signup=get_random_date(), contact=None)
    invitation.competition_types.set([competition_type])
    invitation.categories.set([])
    invitation.documents.set([])
    invitation.qualification_levels.set([])
    return invitation