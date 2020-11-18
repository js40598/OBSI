from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from users.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from users.tasks import refresh_user_blockades
from users.models import UserIncorrectLoginLimit


@login_required
def createuser(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'GET':
        return render(request, 'users/createuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(email=request.POST['email'])
                return render(request, 'users/createuser.html', {'form': UserCreationForm(),
                                                                 'error': "Email address is in use already"})
            except ObjectDoesNotExist or MultipleObjectsReturned:
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
                        blockade = UserIncorrectLoginLimit(user=user, counter=0, is_blocked=False, blockade_expire=None)
                        blockade.save()
                        user.save()
                        return redirect('createuser')
                except IntegrityError:
                    return render(request, 'users/createuser.html', {'form': UserCreationForm(),
                                                                     'error': "The username has already been taken"})
        else:
            return render(request, 'users/createuser.html', {'form': UserCreationForm(),
                                                             'error': "Passwords didn't match"})


def loginuser(request):
    refresh_user_blockades()
    logout(request)
    if request.method == 'GET':
        return render(request, 'users/loginuser.html', {'form': AuthenticationForm()})
    # login form submitted
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # authentication failed
        if user is None:
            # if username correct increase blockade to prevent bruteforce attacks
            try:
                with transaction.atomic():
                    user = User.objects.get(username=request.POST['username'])
                    blockade = UserIncorrectLoginLimit.objects.get(user=user)
                    if not blockade.is_blocked:
                        blockade.counter += 1
                        blockade.save()
                    else:
                        formatted_date = blockade.blockade_expire.strftime('%d/%m/%Y, %H:%M:%S')
                        context = {'form': AuthenticationForm(),
                                   'error': "User is blocked until {}".format(formatted_date)}
                        return render(request, 'users/loginuser.html', context)
            # else pass
            except ObjectDoesNotExist:
                pass
            return render(request, 'users/loginuser.html', {'form': AuthenticationForm(),
                                                            'error': "Authentication failed"})
        # authentication successful
        else:
            # if user is blocked
            try:
                blockade = UserIncorrectLoginLimit.objects.get(user=user, is_blocked=True)
                formatted_date = blockade.blockade_expire.strftime('%d/%m/%Y, %H:%M:%S')
                context = {'form': AuthenticationForm(),
                           'error': "User is blocked until {}".format(formatted_date)}
                return render(request, 'users/loginuser.html', context)
            # if user is not blocked
            except ObjectDoesNotExist:
                # clear blockade and login
                with transaction.atomic():
                    blockade = UserIncorrectLoginLimit.objects.get(user=user)
                    blockade.counter = 0
                    blockade.blockade_expire = None
                    blockade.save()
                login(request, user)
                try:
                    return redirect(request.GET.get('next'))
                except TypeError:
                    return redirect('home')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        return redirect('home')


