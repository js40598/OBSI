from django.db import models
from django.contrib.auth.models import User
from reservation.models import Reservation


class Message(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=1000)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[0:10]


