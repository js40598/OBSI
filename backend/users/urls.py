from django.urls import path
from users import views

urlpatterns = [
    path('login/', views.loginuser, name='loginuser'),
    path('logoutuser/', views.logoutuser, name='logoutuser'),
    path('createuser/', views.createuser, name='createuser'),
]

