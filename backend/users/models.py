from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from users.utils import user_blockade_controller


class UserIncorrectLoginLimit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counter = models.PositiveIntegerField()
    is_blocked = models.BooleanField()
    blockade_expire = models.DateTimeField(null=True, blank=True, default=None)


pre_save.connect(user_blockade_controller, sender=UserIncorrectLoginLimit)
