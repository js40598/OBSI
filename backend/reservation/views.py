from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from calendar import month_name
from calendar import Calendar
from datetime import datetime
from reservation.models import Reservation


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
    reservations = []
    for i in range(1, len(Reservation.TIME_CHOICES)+1):
        try:
            reservations += [Reservation.objects.get(year_slug=year, month_slug=month, day_slug=day, time=i)]
        except ObjectDoesNotExist:
            reservations += [None]
    context = {
        'reservations': reservations,
        'time_choices': Reservation.TIME_CHOICES,
        'current_year': datetime.now().year,
    }
    return render(request, 'reservation/day.html', context)
