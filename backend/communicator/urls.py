from django.urls import path
from communicator import views

urlpatterns = [
    path('<str:room_name>/', views.communicator, name='communicator'),
]
