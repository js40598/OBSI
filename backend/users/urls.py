from django.urls import path
from users import views

urlpatterns = [
    path('signupuser/', views.signupuser, name='signupuser'),
    path('loginuser/', views.loginuser, name='loginuser'),
    path('logoutuser/', views.logoutuser, name='logoutuser'),
]

