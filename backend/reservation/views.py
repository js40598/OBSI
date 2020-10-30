from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from calendar import Calendar
from datetime import datetime


@login_required
def reservation_year(request):
    # Pagination
    current_year = datetime.now().year
    paginator_years = [current_year-1, current_year, current_year+1]
    paginator = Paginator(paginator_years, 1)
    year = request.GET.get('year')
    if year is None:
        year = current_year
    paged_year = paginator.get_page(year)

    # Display
    calendar = [[Calendar().itermonthdays4(current_year, i), i] for i in range(1, 13)]
    context = {
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
    return render(request, 'reservation/day.html')
