from django.db import models
from django.db.models.signals import pre_save
from rooms.utils import room_slug_generator


class Floor(models.Model):
    level = models.IntegerField()

    def __str__(self):
        return str(self.level)


class Room(models.Model):
    DESTINATION_CHOICES = [
        ('ASSEMBLY_HALL', 'Assembly Hall'),
        ('LECTURE', 'Lecture'),
        ('PRACTICALS', 'Practicals')
    ]
    floor = models.ForeignKey(Floor, on_delete=models.DO_NOTHING)
    sign = models.CharField(max_length=100)
    room_slug = models.SlugField(max_length=100, null=True, blank=True, default=None)
    availability_level = models.PositiveIntegerField()
    projector = models.BooleanField()
    multimedia_board = models.BooleanField()
    blackboard = models.BooleanField()
    number_of_places = models.PositiveIntegerField()
    number_of_computers = models.PositiveIntegerField()
    destination = models.CharField(max_length=20, choices=DESTINATION_CHOICES)

    def __str__(self):
        return self.sign


class AdditionalEquipment(models.Model):
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    amount = models.PositiveIntegerField()


pre_save.connect(room_slug_generator, sender=Room)