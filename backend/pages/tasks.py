from pages.models import Reservation
import threading
from datetime import datetime
import pytz


def update_reservation_status():
    res = Reservation.objects.all().filter(is_upcoming=True)
    utc = pytz.UTC
    for reservation in res:
        print(str(reservation.datetime_begin))
        if reservation.datetime_begin < utc.localize(datetime.now()):
            reservation.is_upcoming = False
            reservation.save()
    threading.Timer(60, update_reservation_status).start()
