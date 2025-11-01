from django.views.generic.list import ListView
from django.views.generic import DetailView
from rest_framework.response import Response
from rest_framework import generics

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

class Lifters():
    queryset = Lifter.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        lifters = Lifter.objects.all()
        total_notes = lifters.count()
        if search_param:
            lifters = lifters.filter(title__icontains=search_param)
        serializer = self.serializer_class(lifters[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_notes,
            "page": page_num,
            "last_page": math.ceil(total_notes / limit_num),
            "notes": serializer.data
        })

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

