from django.db import models
from django.contrib.auth.models import User
from rooms.models import Room
from django.db.models.signals import pre_save
from reservation.utils import (reservation_slug_generator,
                               reservation_datetime_generator,
                               reservation_is_upcoming_generator)


class Reservation(models.Model):
    TIME_CHOICES = [
        ('1', '8:00-10:00'),
        ('2', '10:00-12:00'),
        ('3', '12:00-14:00'),
        ('4', '14:00-16:00'),
        ('5', '16:00-18:00'),
        ('6', '18:00-20:00')
    ]
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    slug = models.SlugField(max_length=100, null=True, blank=True, default=None)
    year_slug = models.SlugField(max_length=100, null=True, blank=True, default=None)
    month_slug = models.SlugField(max_length=100, null=True, blank=True, default=None)
    day_slug = models.SlugField(max_length=100, null=True, blank=True, default=None)
    date = models.DateField()
    datetime_begin = models.DateTimeField(null=True, blank=True, default=None)
    time = models.CharField(max_length=12, choices=TIME_CHOICES)
    is_upcoming = models.BooleanField()

    def __str__(self):
        return self.slug


pre_save.connect(reservation_slug_generator, sender=Reservation)
pre_save.connect(reservation_datetime_generator, sender=Reservation)
pre_save.connect(reservation_is_upcoming_generator, sender=Reservation)
