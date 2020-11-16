from django.urls import path, include
from reservation import views

urlpatterns = [
    path('<slug:room_slug>/<int:curr_year>', views.reservation_year, name='reservation_year'),
    path('<slug:room_slug>/<int:year>/<int:month>/<int:day>', views.reservation_day, name='reservation_day'),
    path('<slug:room_slug>/<int:year>/<int:month>/<int:day>/<int:time>/communicator/', include('communicator.urls')),
    # path('communicator/<slug:reservation_slug>', include('communicator.urls')),
]
