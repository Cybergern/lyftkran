""" Create your models here. """
from datetime import datetime
from enum import Enum
from django.db import models

class LifterClass(Enum):
    """Represents a lifters age class"""
    U = "Ungdom"
    J = "Junior"
    S = "Senior"
    M1 = "Veteran (40-49 år)"
    M2 = "Veteran (50-59 år)"
    M3 = "Veteran (60-69 år)"
    M4 = "Veteran (70-79 år)"

class Gender(Enum):
    """Represents a lifters gender"""
    M = "Man"
    F = "Kvinna"

class LicenseStatus(Enum):
    """Represents a license status"""
    LI = "Licensierad"
    EL = "Ej licensierad"

class Role(Enum):
    """Represents a user role within the application"""
    NN = "Ingen roll"
    NA = "Förbundsadministratör"
    DA = "Distriktsadministratör"
    CA = "Föreningsadministratör"

class Lifter(models.Model):
    """Represents a single lifter within the organization"""
    def __str__(self):
        return "%s %s" % (self.first_name, self.family_name)

    first_name = models.CharField(max_length=50)
    family_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    postal_city = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=[(tag.name, tag.value) for tag in Gender])
    id_number = models.CharField(max_length=12)
    club = models.ForeignKey('Club', on_delete=models.DO_NOTHING)
    phone = models.CharField(max_length=50)
    email = models.EmailField()

    created_at = models.DateTimeField(default=datetime.now, editable=False)

class License(models.Model):
    """Represents a single year-long license for a single lifter"""
    def __str__(self):
        return "%s - %s (%s)" % (self.number, self.year, self.requested)
    lifter = models.ForeignKey('Lifter', on_delete=models.DO_NOTHING)
    number = models.CharField(max_length=8)
    year = models.PositiveIntegerField()
    requested = models.DateTimeField(default=datetime.now, blank=True)
    status = models.CharField(max_length=2,
                                      choices=[(tag.name, tag.value) for tag in LicenseStatus])

class District(models.Model):
    """Represents a district"""
    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)

class Club(models.Model):
    """Represents a club"""
    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)
    district = models.ForeignKey('District', on_delete=models.DO_NOTHING)
