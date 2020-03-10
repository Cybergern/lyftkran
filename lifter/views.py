from django.views.generic.list import ListView
from django.views.generic import DetailView

from .models import *


# Create your views here.
class LifterList(ListView):
    model = Lifter
    template_name = 'lifter_list.html'
    lifter_list = Lifter.objects
    context_object_name = 'lifters'
    paginate_by = 20
    ordering = ['family_name', 'first_name']


class LifterDetail(DetailView):
    model = Lifter
    template_name = 'lifter_detail.html'


class ClubList(ListView):
    model = Club
    template_name = 'club_list.html'
    lifter_list = Club.objects
    context_object_name = 'clubs'
    paginate_by = 10
    ordering = ['name']


class ClubDetail(DetailView):
    model = Club
    template_name = 'club_detail.html'

