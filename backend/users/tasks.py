from django.db import transaction

from users.models import UserIncorrectLoginLimit
from datetime import datetime


def refresh_user_blockades():
    for blockade in UserIncorrectLoginLimit.objects.filter(blockade_expire__lte=datetime.now()):
        with transaction.atomic():
            blockade.blockade_expire = None
            blockade.is_blocked = False
            blockade.counter = 0
            blockade.save()
