from reservation.models import Reservation
import threading
from datetime import datetime
import pytz


# check if upcoming reservation dates are in future, if any of them are not, update it
def update_reservation_status():
    res = Reservation.objects.all().filter(is_upcoming=True)
    utc = pytz.UTC
    for reservation in res:
        if reservation.datetime_begin < utc.localize(datetime.now()):
            reservation.is_upcoming = False
            reservation.save()
    threading.Timer(60, update_reservation_status).start()
