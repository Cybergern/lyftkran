""" Create your models here. """
from typing import override
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class LifterClass(models.TextChoices):
    YOUTH = "U", _("Ungdom")
    JUNIOR = "J", _("Junior")
    SENIOR = "S", _("Senior")
    MASTER_1 = "M1", _("Veteran (40-49 år)")
    MASTER_2 = "M2", _("Veteran (50-59 år)")
    MASTER_3 = "M3", _("Veteran (60-69 år)")
    MASTER_4 = "M4", _("Veteran (70-79 år)")


class GenderChoices(models.TextChoices):
    MALE = "M", _("Man") 
    FEMALE = "F", _("Kvinna")


class LicenseStatus(models.TextChoices):
    LICENSED = "L", _("Licensierad")
    NO_LICENSE = "N", _("Ej licensierad")


class JudgeLevel(models.TextChoices):
    DISTRICT_JUDGE = "D", _("Distriktsdomare")
    FEDERATION_JUDGE = "F", _("Förbundsdomare")


class Disciplines(models.TextChoices):
    SQUAT = "S", _("Knäböj")
    BENCHPRESS = "B", _("Bänkpress")
    DEADLIFT = "D", _("Marklyft")
    PARALYMPIC_BENCH = "P", _("Paralympisk Bänkpress")


class CompetitionTypes(models.TextChoices):
    EQUIPPED_BENCH = "EB", _("Utrustad Bänkpress")
    CLASSIC_POWERLIFTING = "CP", _("Klassiskt Styrkelyft")
    EQUIPPED_POWERLIFTING = "EP", _("Utrustat Styrkelyft")
    CLASSIC_BENCHPRESS = "CB", _("Klassisk Bänkpress")
    PARALYMPIC_BENCHPRESS = "PB", _("Paralympisk Bänkpress")


class PointSystems(models.TextChoices):
    IPF_POINTS = "I", _("IPF-poäng")
    WILKS_POINTS = "W", _("Wilks-poäng")


class WeightClass(models.Model):
    min_weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    max_weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    archived = models.BooleanField(default=False)


class AgeBracket(models.Model):
    name = models.CharField(max_length=2, choices=LifterClass.choices)
    min_age = models.PositiveIntegerField()
    max_age = models.PositiveIntegerField()
    archived = models.BooleanField(default=False)


class Category(models.Model):
    gender = models.CharField(max_length=2, choices=GenderChoices.choices)
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
    district = models.ForeignKey("District", on_delete=models.CASCADE, related_name="clubs")
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
    gender = models.CharField(max_length=2, choices=GenderChoices.choices)
    id_number = models.CharField(max_length=12)
    clubs = models.ManyToManyField(Club, related_name="lifters")

    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def get_gender(self) -> GenderChoices:
        return GenderChoices(self.gender)
    
    def get_club_list(self) -> str:
        return ", ".join([x.name for x in self.clubs.all()])


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
    status = models.CharField(max_length=2, choices=LicenseStatus.choices)

    class Meta:
        unique_together = [["number", "year"]]


class JudgeLicense(models.Model):
    def __str__(self):
        return f"{str(self.lifter)}, {self.judge_level} ({self.book_number})"

    lifter = models.ForeignKey("Lifter", on_delete=models.CASCADE, related_name="judge_credentials")
    judge_level = models.CharField(max_length=2, choices=JudgeLevel.choices)
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


class CompetitionType(models.Model):
    name = models.CharField(max_length=3, choices=CompetitionTypes.choices)


class Discipline(models.Model):
    name = models.CharField(max_length=2, choices=Disciplines.choices)
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
    name = models.CharField(max_length=3, choices=PointSystems.choices)


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


class Competition(models.Model):
    invitation = models.ForeignKey("Invitation", on_delete=models.CASCADE)
    results = models.ManyToManyField(CollectedResult)


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


class AbstractAdmin(models.Model):
    class Meta:
           abstract = True

    def can_admin_club(self, club: Club):
        return False
    
    def can_admin_comp(self, competition: Competition):
        return False


class ClubAdmin(AbstractAdmin):
    lifter = models.ForeignKey("Lifter", on_delete=models.CASCADE, related_name="club_admin")
    clubs = models.ManyToManyField(Club)

    @override
    def can_admin_club(self, club: Club):
        return club in self.clubs.all()

    @override
    def can_admin_comp(self, competition: Competition):
        if not competition.invitation.organizer:
            return False
        else:
            return competition.invitation.organizer in self.clubs.all()


class DistrictAdmin(AbstractAdmin):
    lifter = models.ForeignKey("Lifter", on_delete=models.CASCADE, related_name="district_admin")
    districts = models.ManyToManyField(District)

    @override
    def can_admin_club(self, club: Club):
        return club.district in self.districts.all()

    @override
    def can_admin_comp(self, competition: Competition):
        if not competition.invitation.organizer:
            return False
        return competition.invitation.organizer.district in self.districts.all()


class CompetitionAdmin(AbstractAdmin):
    lifter = models.ForeignKey("Lifter", on_delete=models.CASCADE, related_name="competition_admin")
    competitions = models.ManyToManyField(Competition)

    @override
    def can_admin_comp(self, competition: Competition):
        return competition in self.competitions.all()


class CompetitionOrganizer(AbstractAdmin):
    lifter = models.ForeignKey("Lifter", on_delete=models.CASCADE, related_name="competition_organizer")
    competitions = models.ManyToManyField(Competition)

    @override
    def can_admin_comp(self, competition: Competition):
        return competition in self.competitions.all()


class NationalAdmin(AbstractAdmin):
    lifter = models.ForeignKey("Lifter", on_delete=models.CASCADE, related_name="national_admin")

    @override
    def can_admin_club(self, club: Club):
        return True

    @override
    def can_admin_comp(self, competition: Competition):
        return True


class SuperAdmin(AbstractAdmin):
    lifter = models.ForeignKey("Lifter", on_delete=models.CASCADE, related_name="super_admin")

    @override
    def can_admin_club(self, club: Club):
        return True

    @override
    def can_admin_comp(self, competition: Competition):
        return True
