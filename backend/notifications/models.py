from django.db import models
from django.contrib.auth.models import User
from reservation.models import Reservation

# Create your models here.


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    reservation = models.ForeignKey(Reservation, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    is_viewed = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)
