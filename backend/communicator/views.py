from django.shortcuts import render, redirect
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from reservation.models import Reservation
from rooms.models import Room

# Create your views here.


def communicator(request, room_slug, year, month, day, time):
    try:
        reservation = Reservation.objects.get(
                                              year_slug=year,
                                              month_slug=month,
                                              day_slug=day,
                                              time=time)
    except ObjectDoesNotExist:
        return redirect('reservation_day', year, month, day)
    context = {
        'room_slug': room_slug,
        'current_year': datetime.now().year,
    }
    return render(request, 'communicator/communicator.html', context)
