from django.db import models
from datetime import datetime
from enum import Enum
# Create your models here.

class LifterClass(Enum):
    U = "Ungdom"
    J = "Junior"
    S = "Senior"
    M1 = "Veteran (40-49 år)"
    M2 = "Veteran (50-59 år)"
    M3 = "Veteran (60-69 år)"
    M4 = "Veteran (70-79 år)"

class Gender(Enum):
    M = "Man"
    F = "Kvinna"

class LicenseStatus(Enum):
    LI = "Licensierad"
    EL = "Ej licensierad"

class Role(Enum):
    NN = "Ingen roll"
    NA = "Förbundsadministratör"
    DA = "Distriktsadministratör"
    CA = "Föreningsadministratör"

class Lifter(models.Model):
    def __str__(self):
        return self.first_name + " " + self.family_name

    def getCurrentLicense(self):
        return License.objects.filter(lifter=self)

    first_name = models.CharField(max_length=50)
    family_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    postal_city = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=[(tag.name, tag.value) for tag in Gender])
    id_number = models.CharField(max_length=12)
    club = models.ForeignKey('Club', on_delete=models.DO_NOTHING)
    district = models.ForeignKey('District', on_delete=models.DO_NOTHING)
    phone = models.CharField(max_length=50)
    email = models.EmailField()

    created_at = models.DateTimeField(default=datetime.now, editable=False)

class License(models.Model):
    def __str__(self):
        return self.license_number + " - " + self.license_year
    lifter = models.ForeignKey('Lifter', on_delete=models.DO_NOTHING)
    license_number = models.CharField(max_length=8)
    license_year = models.PositiveIntegerField()
    license_requested = models.DateTimeField(default=datetime.now, blank=True)
    license_status = models.CharField(max_length=2, choices=[(tag.name, tag.value) for tag in LicenseStatus])

class District(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)

class Club(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)