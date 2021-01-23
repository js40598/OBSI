from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import logout
from reservation.tasks import update_reservation_status
from reservation.models import Reservation
from datetime import datetime
from rooms.models import Room, Floor
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


# landing page
def landing(request):
    logout(request)
    return render(request, 'pages/landing.html')


@login_required
def home(request):
    update_reservation_status()
    context = {
        'current_year': datetime.now().year,
        'user': request.user,
    }
    return render(request, 'pages/index.html', context)


@login_required
def search(request):
    # get all available floors
    floor_choices = [int(floor.level) for floor in Floor.objects.all().order_by('-level')]
    context = {
        'current_year': datetime.now().year,
        'destination_choices': Room.DESTINATION_CHOICES,
        'floor_choices': floor_choices,
        'time_choices': Reservation.TIME_CHOICES,
    }
    output_rooms = []
    exact_date = True
    rooms = Room.objects.all()
    if request.method == 'GET':
        context['rooms'] = rooms
        return render(request, 'pages/search.html', context)
    else:
        context['values'] = request.POST
        # filter search requirements
        if 'sign' in request.POST:
            if request.POST['sign']:
                rooms = rooms.filter(sign=request.POST['sign'])
        if 'places' in request.POST:
            if request.POST['places']:
                rooms = rooms.filter(number_of_places__gte=request.POST['places'])
        if 'computers' in request.POST:
            if request.POST['computers']:
                rooms = rooms.filter(number_of_computers__gte=request.POST['computers'])
        if 'floor' in request.POST:
            if request.POST['floor']:
                rooms = rooms.filter(floor__level=request.POST['floor'])
        if 'destination' in request.POST:
            if request.POST['destination']:
                rooms = rooms.filter(destination=request.POST['destination'])
        if 'projector' in request.POST:
            if request.POST['projector']:
                rooms = rooms.filter(projector=True)
        if 'multimedia_board' in request.POST:
            if request.POST['multimedia_board']:
                rooms = rooms.filter(multimedia_board=True)
        if 'blackboard' in request.POST:
            if request.POST['blackboard']:
                rooms = rooms.filter(blackboard=True)
        if 'date' in request.POST and 'time' in request.POST:
            if request.POST['date'] and request.POST['time']:
                date = datetime.strptime(request.POST['date'], '%Y-%m-%d')
                context['date'] = date
                for room in rooms:
                    try:
                        Reservation.objects.get(room=room,
                                                year_slug=date.year,
                                                month_slug=date.month,
                                                day_slug=date.day,
                                                time=request.POST['time'])
                    except ObjectDoesNotExist:
                        output_rooms += [room]
            elif request.POST['date'] and not request.POST['time']:
                date = datetime.strptime(request.POST['date'], '%Y-%m-%d')
                for room in rooms:
                    day_available_counter = 0
                    for time_choice in Reservation.TIME_CHOICES:
                        try:
                            Reservation.objects.get(room=room,
                                                    year_slug=date.year,
                                                    month_slug=date.month,
                                                    day_slug=date.day,
                                                    time=time_choice[0])
                            day_available_counter += 1
                        except ObjectDoesNotExist:
                            pass
                    if day_available_counter != len(Reservation.TIME_CHOICES):
                        print(room.sign)
                        output_rooms += [room]
                context['date'] = date
            elif not request.POST['date'] and request.POST['time']:
                context['error'] = 'If Time is chosen Date must be too'
                context['exact_date'] = False
                return render(request, 'pages/search.html', context)
            else:
                exact_date = False
                output_rooms = rooms

    context['rooms'] = output_rooms
    context['exact_date'] = exact_date
    return render(request, 'pages/search.html', context)
