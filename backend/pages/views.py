from django.shortcuts import render
from reservation.tasks import update_reservation_status
from datetime import datetime

# Create your views here.


def home(request):
    update_reservation_status()
    context = {
        'current_year': datetime.now().year,
        'user': request.user,
    }
    return render(request, 'pages/index.html', context)
