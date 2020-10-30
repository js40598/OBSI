from django.shortcuts import render, redirect
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from reservation.models import Reservation

# Create your views here.


def communicator(request, year, month, day, time):
    try:
        reservation = Reservation.objects.get(year_slug=year,
                                              month_slug=month,
                                              day_slug=day,
                                              time=time)
    except ObjectDoesNotExist:
        return redirect('reservation_day', year, month, day)
    context = {
        'current_year': datetime.now().year,
    }
    return render(request, 'communicator/communicator.html', context)
