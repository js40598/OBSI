from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from reservation.models import Reservation
from rooms.models import Room
from communicator.models import Message
from backend.settings import TIME_ZONE


def communicator(request, room_slug, year, month, day, time, room_name):
    reservation = Reservation.objects.get(room__room_slug=room_slug,
                                          year_slug=year,
                                          month_slug=month,
                                          day_slug=day,
                                          time=time)
    messages = [[datetime.strftime(message.datetime + timedelta(hours=1), '%d/%m/%Y %H:%M'), message]
                for message in Message.objects.filter(reservation=reservation)]
    context = {
        'messages': messages,
        # 'communicator_instance_path': f'{room_slug}/{year}/{month}/{day}/{time}',
        # 'room_name': reservation.reservation_slug,
        # 'room_name': reservation.reservation_slug,
        'room_name': room_name,
        'datetime': datetime.now(),
        'current_year': datetime.now().year,
    }
    return render(request, 'communicator/communicator.html', context)
