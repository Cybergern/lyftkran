from django.core.management.base import BaseCommand

from lifter.test.tools import create_all_districts, create_club, create_lifter, get_random_club_list


def make_test_data():
    create_all_districts()
    for x in range(0, 20):
        create_club()
    for x in range(0, 100):
        create_lifter(get_random_club_list())


class Command(BaseCommand):

    def handle(self, *args, **options):
        make_test_data()
