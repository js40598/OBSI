from django.urls import path
from reservation import views

urlpatterns = [
    path('', views.reservation_year, name='reservation_year'),
]

