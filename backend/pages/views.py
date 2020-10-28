from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from backend.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from pages.tasks import update_reservation_status
from pages.models import Floor, Room
from django.db import transaction

# Create your views here.


def home(request):
    update_reservation_status()
    return render(request, 'pages/index.html')




def signupuser(request):
    if request.method == 'GET':
        return render(request, 'pages/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=request.POST['username'],
                        password=request.POST['password1'],
                        email=request.POST['email'],
                        first_name=request.POST['first_name'],
                        last_name=request.POST['first_name'],

                    )
                    group = Group.objects.get(id=request.POST['groups'])
                    group.user_set.add(user)
                    user.save()
                    if group.name == 'Staff':
                        user.is_staff = True
                        user.save()
                    return redirect('home')
            except IntegrityError:
                return render(request, 'pages/signupuser.html', {'form': UserCreationForm(),
                                                                 'error': "The username has already been taken"})
        else:
            return render(request, 'pages/signupuser.html', {'form': UserCreationForm(),
                                                             'error': "Passwords didn't match"})
