from django.test import TestCase
import pytest
from lifter.models import (AbstractAdmin, Club, ClubAdmin, Competition, CompetitionAdmin, District, DistrictAdmin, 
                           Lifter, NationalAdmin, SuperAdmin)
from lifter.test.tools import create_all_districts, create_club, create_competition, create_lifter

# Create your tests here.

class AdminTests(TestCase):

    def create_test_base(self):
        create_all_districts()
        self.districts = District.objects.all()
        self.admin_district = self.districts[0]
        self.non_admin_district = self.districts[1]
        self.admin_club = create_club(self.admin_district)
        self.other_club_same_district = create_club(self.admin_district)
        self.non_admin_club = create_club(self.non_admin_district)
        self.club_admin = ClubAdmin.objects.create(lifter=create_lifter(clubs=[self.admin_club]))
        self.club_admin.clubs.set([self.admin_club])
        self.district_admin = DistrictAdmin.objects.create(lifter=create_lifter(clubs=[self.admin_club]))
        self.district_admin.districts.set([self.admin_district])
        self.admin_competition = create_competition(self.admin_club)
        self.other_competition = create_competition(self.other_club_same_district)
        self.non_admin_competition = create_competition(self.non_admin_club)
        self.competition_admin = CompetitionAdmin.objects.create(lifter=create_lifter(clubs=[self.admin_club]))
        self.competition_admin.competitions.set([self.admin_competition])
        self.national_admin = NationalAdmin.objects.create(lifter=create_lifter(clubs=[self.admin_club]))
        self.super_admin = SuperAdmin.objects.create(lifter=create_lifter(clubs=[self.admin_club]))

    def setUp(self):
        self.create_test_base()


    @pytest.mark.django_db
    def test_club_admin_accessibility(self):
        assert self.club_admin.can_admin_club(self.admin_club) == True
        assert self.club_admin.can_admin_club(self.other_club_same_district) == False    
        assert self.club_admin.can_admin_club(self.non_admin_club) == False

        assert self.district_admin.can_admin_club(self.admin_club) == True
        assert self.district_admin.can_admin_club(self.other_club_same_district) == True    
        assert self.district_admin.can_admin_club(self.non_admin_club) == False

        assert self.competition_admin.can_admin_club(self.admin_club) == False
        assert self.competition_admin.can_admin_club(self.other_club_same_district) == False    
        assert self.competition_admin.can_admin_club(self.non_admin_club) == False

        assert self.national_admin.can_admin_club(self.admin_club) == True
        assert self.national_admin.can_admin_club(self.other_club_same_district) == True
        assert self.national_admin.can_admin_club(self.non_admin_club) == True

        assert self.super_admin.can_admin_club(self.admin_club) == True
        assert self.super_admin.can_admin_club(self.other_club_same_district) == True
        assert self.super_admin.can_admin_club(self.non_admin_club) == True

    @pytest.mark.django_db
    def test_comp_admin_accessibility(self):
        assert self.club_admin.can_admin_comp(self.admin_competition) == True
        assert self.club_admin.can_admin_comp(self.other_competition) == False
        assert self.club_admin.can_admin_comp(self.non_admin_competition) == False

        assert self.district_admin.can_admin_comp(self.admin_competition) == True
        assert self.district_admin.can_admin_comp(self.other_competition) == True
        assert self.district_admin.can_admin_comp(self.non_admin_competition) == False

        assert self.competition_admin.can_admin_comp(self.admin_competition) == True
        assert self.competition_admin.can_admin_comp(self.other_competition) == False
        assert self.competition_admin.can_admin_comp(self.non_admin_competition) == False

        assert self.national_admin.can_admin_comp(self.admin_competition) == True
        assert self.national_admin.can_admin_comp(self.other_competition) == True
        assert self.national_admin.can_admin_comp(self.non_admin_competition) == True

        assert self.super_admin.can_admin_comp(self.admin_competition) == True
        assert self.super_admin.can_admin_comp(self.other_competition) == True
        assert self.super_admin.can_admin_comp(self.non_admin_competition) == True
