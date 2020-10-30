from django.urls import path
from reservation import views

urlpatterns = [
    path('<slug:slug>', views.reservation_year, name='reservation_year'),
]

