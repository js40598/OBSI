from django.urls import path
from communicator import views

urlpatterns = [
    path('', views.communicator, name='communicator')
]

