from django.urls import path
from reservation import views

urlpatterns = [
    path('<int:curr_year>', views.reservation_year, name='reservation_year'),
    path('<int:year>/<int:month>/<int:day>', views.reservation_day, name='reservation_day'),
]

