import random
from datetime import datetime
import time
from enum import Enum
from random import randint

from autofixture import AutoFixture
from django.core.management.base import BaseCommand

from lifter.models import (Club, District, Gender, License, LicenseStatus,
                           Lifter, LifterClass)


class TestDataGenerator():

    first_name_choices = ("Björn", "Johanna", "Leslie", "Kim",
                          "Stefan", "Göran", "My", "Linnea", "Maria", "Hampus")
    family_name_choices = ("Karlsson", "Persson", "Marquis", "May", "Merkel", "Johansson", "Gustafsson",
                           "Thyberg", "Olsson", "Björkman")
    city_name_choices = ("Målilla", "Halmstad", "Stockholm",
                         "Göteborg", "Karlstad", "Örebro", "Västerås", "Malmö")
    club_suffix_choices = ("SK", "TK", "AK", "KK", "IK", "IF")
    districts = ("Mellersta Norrlands SDF", "Norra Norrlands SDF", "Sydsvenska SDF", "Sydöstra SDF", "Södra Norrlands SDF",
                 "Västra Götalands SDF", "Västra Svealands SDF", "Östra Svealands SDF")
    road_base = ("Tiger", "Löv", "Folkunga", "Kungs", "Drottning",
                 "Vikinga", "Gran", "Kyrko", "Katedral")
    road_suffix = ("vägen", "gatan", "avenyn", "gränd")

    def get_random_date(self):
        return datetime.strptime("%i-%i-%i" % (randint(1970, 2005), randint(1, 12), randint(1, 28)), "%Y-%m-%d")

    def get_random_id(self):
        date = self.get_random_date()
        personal_number = date.strftime("%Y%m%d") + str(randint(100, 999))
        full_sum = 0
        for x in range(0, len(personal_number[2:])):
            prod = (2 - (x % 2)) * int(personal_number[2:][x])
            full_sum += sum([int(d) for d in str(prod)])
        control_number = (10 - (full_sum % 10)) % 10
        return personal_number + str(control_number)

    def get_random_club_name(self):
        return random.choice(self.city_name_choices) + " " + random.choice(self.club_suffix_choices)

    def get_random_name_and_email(self):
        first_name = random.choice(self.first_name_choices)
        family_name = random.choice(self.family_name_choices)
        email = "%s.%s@gmail.com" % (first_name, family_name)
        return (first_name, family_name, email)

    def get_random_address(self):
        return "%s%s %s" % (random.choice(self.road_base), random.choice(self.road_suffix), str(randint(1, 99)))

    def get_random_postal_code(self):
        return randint(10000, 99999)

    def get_random_phone(self):
        return "070-" + str(randint(1000000, 9999999))

    def get_random_city(self):
        return random.choice(self.city_name_choices)

    def create_all_districts(self):
        for dis_name in self.districts:
            District.objects.create(name=dis_name)

    def create_club(self):
        Club.objects.create(name=self.get_random_club_name(
        ), district=random.choice(District.objects.all()))

    def create_lifter(self):
        name_and_email = self.get_random_name_and_email()
        lifter = Lifter.objects.create(first_name=name_and_email[0], family_name=name_and_email[1], address=self.get_random_address(),
                                       postal_code=self.get_random_postal_code(), postal_city=self.get_random_city(),
                                       gender=random.choice(list(Gender)).name, id_number=self.get_random_id(),
                                       club=random.choice(Club.objects.all()), phone=self.get_random_phone(), email=name_and_email[2])
        self.create_licenses(lifter)

    def create_licenses(self, license_lifter):
        year_now = int(datetime.now().strftime("%Y"))
        for x in range(year_now - 2, year_now + 1):
            license_number = license_lifter.id_number[2:8] + license_lifter.first_name[0].lower(
            ) + license_lifter.family_name[0].lower()
            license_year = x
            license_status = random.choice(list(LicenseStatus)).name
            License.objects.create(
                lifter=license_lifter, number=license_number, year=license_year, status=license_status)

    def make_test_data(self):
        self.create_all_districts()
        for x in range(0, 20):
            self.create_club()
        for x in range(0, 100):
            self.create_lifter()


class Command(BaseCommand):

    def handle(self, *args, **options):
        TestDataGenerator().make_test_data()
