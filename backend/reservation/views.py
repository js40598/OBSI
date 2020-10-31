from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from calendar import month_name
from calendar import Calendar
from datetime import date, datetime
from reservation.models import Reservation
from rooms.models import Room


@login_required
def reservation_year(request, curr_year):
    # Pagination
    current_year = datetime.now().year
    paginator_years = [current_year-1, current_year, current_year+1]
    paginator = Paginator(paginator_years, 1)
    year = request.GET.get('year')
    if year is None:
        year = current_year
    paged_year = paginator.get_page(year)

    # Display
    calendar = [[Calendar().itermonthdays4(curr_year, i), i, month_name[i]] for i in range(1, 13)]
    context = {
        'curr_year': curr_year,
        'dates': Calendar(),
        'current_year': current_year,
        'paged_year': paged_year,
        'paginator_years': paginator_years,
        'year': int(year),
        'calendar': calendar,
    }

    return render(request, 'reservation/year.html', context)


@login_required
def reservation_day(request, year, month, day):
    time_choices = Reservation.TIME_CHOICES
    reservations = []
    for i in range(1, len(Reservation.TIME_CHOICES)+1):
        try:
            reservations += [[True,
                              Reservation.objects.get(year_slug=year, month_slug=month, day_slug=day, time=i),
                              time_choices[i-1]
                              ]]
        except ObjectDoesNotExist:
            reservations += [[False, time_choices[i-1]]]
    if request.method == 'POST':
        if 'create_reservation' in request.POST:
            try:
                Reservation.objects.get(user=request.user,
                                        year_slug=year,
                                        month_slug=month,
                                        day_slug=day,
                                        time=request.POST['time'])
            except ObjectDoesNotExist:
                new_reservation = Reservation(user=request.user,
                                              room=Room.objects.get(sign=100),
                                              date=date(year, month, day),
                                              time=request.POST['time'])
                new_reservation.save()
                return redirect('reservation_day', year, month, day)
        elif 'remove_reservation' in request.POST:
            remove_reservation = Reservation.objects.get(user=request.user,
                                                         year_slug=year,
                                                         month_slug=month,
                                                         day_slug=day,
                                                         time=request.POST['time'])
            remove_reservation.delete()
            return redirect('reservation_day', year, month, day)
    context = {
        'reservations': reservations,
        'time_choices': time_choices,
        'current_year': datetime.now().year,
    }
    return render(request, 'reservation/day.html', context)
