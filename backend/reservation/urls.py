from django.urls import path, include
from reservation import views

urlpatterns = [
    path('<int:curr_year>', views.reservation_year, name='reservation_year'),
    path('<int:year>/<int:month>/<int:day>', views.reservation_day, name='reservation_day'),
    path('<int:year>/<int:month>/<int:day>/<int:time>/communicator', include('communicator.urls')),
]

