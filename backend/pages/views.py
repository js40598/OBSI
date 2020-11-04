from django.shortcuts import render
from reservation.tasks import update_reservation_status
from datetime import datetime
from rooms.models import Room, Floor

# Create your views here.


def home(request):
    update_reservation_status()
    context = {
        'current_year': datetime.now().year,
        'user': request.user,
    }
    return render(request, 'pages/index.html', context)


def search(request):
    floor_choices = [floor.level for floor in Floor.objects.all().order_by('-level')]
    rooms = Room.objects.all()
    if request.method == "POST":
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
    context = {
        'current_year': datetime.now().year,
        'rooms': rooms,
        'destination_choices': Room.DESTINATION_CHOICES,
        'floor_choices': floor_choices
    }
    return render(request, 'pages/search.html', context)
