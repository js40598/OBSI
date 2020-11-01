def room_slug_generator(sender, instance, *args, **kwargs):
    instance.room_slug = instance.sign