from datetime import datetime


def reservation_slug_generator(sender, instance, *args, **kwargs):
    instance.slug = '{}_{}_{}'.format(instance.room.sign, str(instance.date), str(instance.time))


def reservation_datetime_generator(sender, instance, *args, **kwargs):
    TIME_DICTIONARY = {
        '1': '08 00 00',
        '2': '10 00 00',
        '3': '12 00 00',
        '4': '14 00 00',
        '5': '16 00 00',
        '6': '18 00 00',
    }
    instance.datetime_begin = datetime.strptime(
        '{} {}'.format(instance.date, TIME_DICTIONARY[instance.time]),
        '%Y-%m-%d %H %M %S'
    ).strftime('%Y-%m-%d %H:%M:%S')


def reservation_is_upcoming_generator(sender, instance, *args, **kwargs):
    if datetime.strptime(instance.datetime_begin, '%Y-%m-%d %H:%M:%S') > datetime.now():
        instance.is_upcoming = True
    else:
        instance.is_upcoming = False
