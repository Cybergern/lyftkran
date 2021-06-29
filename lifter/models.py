""" Create your models here. """
from enum import Enum
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class LifterClass(Enum):
    U = "Ungdom"
    J = "Junior"
    S = "Senior"
    M1 = "Veteran (40-49 år)"
    M2 = "Veteran (50-59 år)"
    M3 = "Veteran (60-69 år)"
    M4 = "Veteran (70-79 år)"


class GenderChoices(Enum):
    M = "Man"
    F = "Kvinna"


class LicenseStatus(Enum):
    LI = "Licensierad"
    EL = "Ej licensierad"


class JudgeLevel(Enum):
    DD = "Distriktsdomare"
    FD = "Förbundsdomare"


class Disciplines(Enum):
    SQ = "Knäböj"
    BP = "Bänkpress"
    DL = "Marklyft"
    PB = "Paralympisk Bänkpress"


class CompetitionTypes(Enum):
    EBP = "Utrustad Bänkpress"
    CPL = "Klassiskt Styrkelyft"
    EPL = "Utrustat Styrkelyft"
    CBP = "Klassisk Bänkpress"
    PBP = "Paralympisk Bänkpress"


class PointSystems(Enum):
    IPF = "IPF-poäng"
    WLK = "Wilks-poäng"


class WeightClass(models.Model):
    min_weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    max_weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    archived = models.BooleanField(default=False)


class AgeBracket(models.Model):
    name = models.CharField(max_length=2, choices=[(tag.name, tag.value) for tag in LifterClass])
    min_age = models.PositiveIntegerField()
    max_age = models.PositiveIntegerField()
    archived = models.BooleanField(default=False)


class Category(models.Model):
    gender = models.CharField(max_length=2, choices=[(tag.name, tag.value) for tag in GenderChoices])
    weight_class = models.ForeignKey("WeightClass", on_delete=models.CASCADE, related_name="weight_categories")
    age_bracket = models.ForeignKey("AgeBracket", on_delete=models.CASCADE, related_name="age_categories")


class Fee(models.Model):
    year = models.PositiveIntegerField()
    invoiced_at = models.DateTimeField(blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)


class Club(models.Model):
    """Represents a club"""
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    district = models.ForeignKey("District", on_delete=models.CASCADE)
    rf_number = models.PositiveIntegerField(blank=True, null=True)
    org_number = models.CharField(max_length=10, blank=True, null=True)
    contact_information = models.ForeignKey("ContactInformation", on_delete=models.CASCADE)
    fees = models.ManyToManyField(Fee)


class Lifter(models.Model):
    """Represents a single lifter within the organization"""
    def __str__(self):
        return "%s %s" % (self.first_name, self.family_name)

    first_name = models.CharField(max_length=50)
    family_name = models.CharField(max_length=100)
    contact_information = models.ForeignKey("ContactInformation", on_delete=models.CASCADE)
    gender = models.CharField(max_length=2, choices=[(tag.name, tag.value) for tag in GenderChoices])
    id_number = models.CharField(max_length=12)
    clubs = models.ManyToManyField(Club, related_name="lifters")

    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def gender_name(self):
        if self.gender == GenderChoices.F:
            return GenderChoices.F.value
        else:
            return GenderChoices.M.value


class License(models.Model):
    """Represents a single year-long license for a single lifter"""
    def __str__(self):
        return "%s - %s (%s)" % (self.number, self.year, self.requested.strftime("%Y-%m-%d %H:%M"))
    lifter = models.ForeignKey("Lifter", on_delete=models.CASCADE, related_name="licenses")
    club = models.ForeignKey("Club", on_delete=models.DO_NOTHING, related_name="licenses")
    number = models.CharField(max_length=8)
    year = models.PositiveIntegerField()
    requested = models.DateTimeField(default=timezone.now, blank=True)
    canceled_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=2, choices=[(tag.name, tag.value) for tag in LicenseStatus])

    class Meta:
        unique_together = [["number", "year"]]


class JudgeLicense(models.Model):
    def __str__(self):
        return f"{str(self.lifter)}, {self.judge_level} ({self.book_number})"

    lifter = models.ForeignKey("Lifter", on_delete=models.CASCADE, related_name="judge_credentials")
    judge_level = models.CharField(max_length=2, choices=[(tag.name, tag.value) for tag in JudgeLevel])
    book_number = models.PositiveIntegerField()
    approved = models.BooleanField()
    year = models.PositiveIntegerField()


class Contact(models.Model):
    role = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)


class District(models.Model):
    """Represents a district"""
    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)
    rf_number = models.PositiveIntegerField(blank=True, null=True)
    org_number = models.CharField(max_length=10, blank=True, null=True)
    contact_information = models.ForeignKey("ContactInformation", on_delete=models.CASCADE)
    contacts = models.ManyToManyField(Contact)


class ContactInformation(models.Model):
    address = models.CharField(max_length=200, blank=True, null=True)
    postal_code = models.CharField(max_length=5, blank=True, null=True)
    postal_city = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)


class ClubAdmin(models.Model):
    lifter = models.ForeignKey("Lifter", on_delete=models.CASCADE, related_name="club_admin")
    clubs = models.ManyToManyField(Club)


class DistrictAdmin(models.Model):
    lifter = models.ForeignKey("Lifter", on_delete=models.CASCADE, related_name="district_admin")
    districts = models.ManyToManyField(District)


class NationalAdmin(models.Model):
    lifter = models.ForeignKey("Lifter", on_delete=models.CASCADE, related_name="national_admin")


class CompetitionAdmin(models.Model):
    lifter = models.ForeignKey("Lifter", on_delete=models.CASCADE, related_name="competition_admin")


class CompetitionOrganizer(models.Model):
    lifter = models.ForeignKey("Lifter", on_delete=models.CASCADE, related_name="competition_organizer")


class SuperAdmin(models.Model):
    lifter = models.ForeignKey("Lifter", on_delete=models.CASCADE, related_name="super_admin")


class CompetitionType(models.Model):
    name = models.CharField(max_length=3, choices=[(tag.name, tag.value) for tag in CompetitionTypes])


class Discipline(models.Model):
    name = models.CharField(max_length=2, choices=[(tag.name, tag.value) for tag in Disciplines])
    competition_type = models.ManyToManyField(CompetitionType)


class Round(models.Model):
    division = models.ForeignKey("Division", on_delete=models.CASCADE, related_name="rounds")


class CollectedResult(models.Model):
    lifter = models.ForeignKey("Lifter", on_delete=models.CASCADE, related_name="results")
    weighin_weight = models.DecimalField(max_digits=5, decimal_places=2)
    weight_class = models.ForeignKey("WeightClass", on_delete=models.CASCADE, related_name="results")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="results")


class Result(models.Model):
    removed = models.BooleanField(default=False)
    order_number = models.PositiveIntegerField(blank=True, null=True)
    result = models.DecimalField(max_digits=4, decimal_places=1)
    discipline = models.ForeignKey("Discipline", on_delete=models.CASCADE)
    collected_result = models.ForeignKey("CollectedResult", on_delete=models.CASCADE,
                                         related_name="individual_results")


class SeriesTeamResult(models.Model):
    team = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="team_results")
    round = models.ForeignKey("Round", on_delete=models.CASCADE, related_name="results")
    results = models.ManyToManyField(Result)


class PointSystem(models.Model):
    name = models.CharField(max_length=3, choices=[(tag.name, tag.value) for tag in PointSystems])


class Division(models.Model):
    name = models.CharField(max_length=100)
    start = models.DateField()
    stop = models.DateField()
    max_lifters = models.PositiveIntegerField()
    competition_type = models.ForeignKey("CompetitionType", on_delete=models.CASCADE)
    point_system = models.ForeignKey("PointSystem", on_delete=models.CASCADE)


class Team(models.Model):
    club = models.ForeignKey("Club", on_delete=models.CASCADE)
    division = models.ForeignKey("Division", on_delete=models.DO_NOTHING, related_name="teams")


class Document(models.Model):
    file = models.FileField()


class QualificationLevels(models.Model):
    category = models.ForeignKey("Category", on_delete=models.DO_NOTHING)
    qualification_limit = models.PositiveIntegerField()

class Invitation(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    organizer = models.ForeignKey("Club", on_delete=models.SET_NULL, blank=True, null=True)
    start_date = models.DateField()
    finish_date = models.DateField()
    last_signup = models.DateField()
    contact = models.ForeignKey("Contact", on_delete=models.SET_NULL, blank=True, null=True)
    competition_types = models.ManyToManyField(CompetitionType)
    categories = models.ManyToManyField(Category)
    documents = models.ManyToManyField(Document)
    qualification_levels = models.ManyToManyField(QualificationLevels)
    affects_ranking = models.BooleanField(default=True)


class Competition(models.Model):
    invitation = models.ForeignKey("Invitation", on_delete=models.CASCADE)
    results = models.ManyToManyField(CollectedResult)
