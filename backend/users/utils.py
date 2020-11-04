from datetime import datetime, timedelta


def user_blockade_controller(sender, instance, *args, **kwargs):
    if instance.counter >= 5:
        instance.is_blocked = True
        instance.blockade_expire = datetime.now() + timedelta(hours=1)
