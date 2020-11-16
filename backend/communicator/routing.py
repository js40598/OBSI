# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'(?P<room_name>\w+)/',
            consumers.ChatConsumer.as_asgi()),
    # re_path(r'reservation/'
    #         r'(?P<room_slug>\w+)/'
    #         r'(?P<year_slug>\w+)/'
    #         r'(?P<month_slug>\w+)/'
    #         r'(?P<day_slug>\w+)/'
    #         r'(?P<time_slug>\w+)/'
    #         r'(?P<room_name>\w+)/',
    #         consumers.ChatConsumer.as_asgi()),
    # re_path(r'^reservation/communicator/(?P<reservation_slug>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]