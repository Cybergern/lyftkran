from django.urls import path
from .views import LifterList
from .views import LifterDetail

urlpatterns = [
    path('lifters/', LifterList.as_view()),
    path('<int:pk>/', LifterDetail.as_view()),
]