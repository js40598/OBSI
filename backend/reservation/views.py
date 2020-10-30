from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from calendar import Calendar
from datetime import datetime


@login_required
def reservation_year(request, year_slug=datetime.now().year):

    context = {
        'dates': Calendar()
    }
    return render(request, 'reservation/year.html', context)
