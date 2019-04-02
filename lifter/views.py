from django.shortcuts import render
from django.http import HttpResponse

from .models import Lifter

# Create your views here.
def index(request):
    #return HttpResponse('Index method')
    lifters = Lifter.objects.order_by('family_name')
    return render(request, 'lifter/index.html', {
        'lifters': lifters
    })