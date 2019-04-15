from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.core.paginator import Paginator

from .models import *

# Create your views here.
class LifterList(ListView):
    model = Lifter
    template_name = 'lifter_list.html'
    lifter_list = Lifter.objects.order_by('family_name')
    context_object_name = 'lifters'
    paginate_by = 20

class LifterDetail(DetailView):
    model = Lifter
    template_name = 'lifter_detail.html'

class ClubList(ListView):
    model = Club
    template_name = 'club_list.html'
    lifter_list = Club.objects.order_by('name')
    context_object_name = 'clubs'
    paginate_by = 10

class ClubDetail(DetailView):
    model = Club
    template_name = 'club_detail.html'

