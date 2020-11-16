from django.shortcuts import render, redirect
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from reservation.models import Reservation
from rooms.models import Room

# Create your views here.

#
# def room(request, room_name):
#     return render(request, 'communicator/room.html', {
#         'room_name': room_name
#     })

#
# def communicator(request, room_name):
#     # reservation = Reservation.objects.get(reservation_slug=reservation_slug)
#     context = {
#         # 'room_name': f'{room_slug}/{year}/{month}/{day}/{time}/communicator',
#         # 'room_name': reservation_slug,
#         'room_name': room_name,
#         'current_year': datetime.now().year,
#     }
#     return render(request, 'communicator/communicator.html', context)
#

def communicator(request, room_slug, year, month, day, time, room_name):
    reservation = Reservation.objects.get(room__room_slug=room_slug,
                                          year_slug=year,
                                          month_slug=month,
                                          day_slug=day,
                                          time=time)
    context = {
        'communicator_instance_path': f'{room_slug}/{year}/{month}/{day}/{time}',
        # 'room_name': reservation.reservation_slug,
        # 'room_name': reservation.reservation_slug,
        'room_name': room_name,
        'datetime': datetime.now(),
        'current_year': datetime.now().year,
    }
    return render(request, 'communicator/communicator.html', context)


# def room(request, room_name):
#     context = {
#         'room_name': room_name
#     }
#     return render(request, 'communicator/communicator.html', context)
