from django.urls import path
from .views import *

urlpatterns = [
    path('lifters/', LifterList.as_view()),
    path('lifters/<int:pk>/', LifterDetail.as_view()),
    path('clubs/', ClubList.as_view()),
    path('clubs/<int:pk>/', ClubDetail.as_view()),
]