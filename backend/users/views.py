from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from users.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.db import transaction
from django.contrib.auth.decorators import login_required


@login_required
def createuser(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'GET':
        return render(request, 'users/createuser.html', {'form': UserCreationForm()})
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
                    if 'is_lecturer' in request.POST:
                        group = Group.objects.get(name='Lecturer')
                    else:
                        group = Group.objects.get(name='Student')
                    group.user_set.add(user)
                    user.save()
                    return redirect('home')
            except IntegrityError:
                return render(request, 'users/createuser.html', {'form': UserCreationForm(),
                                                                 'error': "The username has already been taken"})
        else:
            return render(request, 'users/createuser.html', {'form': UserCreationForm(),
                                                             'error': "Passwords didn't match"})


def loginuser(request):
    logout(request)
    if request.method == 'GET':
        return render(request, 'users/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'users/loginuser.html', {'form': AuthenticationForm()})
        else:
            login(request, user)
            return redirect('home')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        return redirect('home')


