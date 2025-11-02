from django.urls import path
from lifter import views

urlpatterns = [
    path('lifters/', views.LifterList.as_view()),
    path('lifters/<int:pk>/', views.LifterDetail.as_view()),
    path('clubs/', views.ClubList.as_view()),
    path('clubs/<int:pk>/', views.ClubDetail.as_view()),
]