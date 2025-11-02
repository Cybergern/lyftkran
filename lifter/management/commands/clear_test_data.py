from django.core.management import BaseCommand

from lifter.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        License.objects.all().delete()
        Lifter.objects.all().delete()
        ContactInformation.objects.all().delete()
        Club.objects.all().delete()
        District.objects.all().delete()
