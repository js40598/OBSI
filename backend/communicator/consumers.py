# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from communicator.models import Message
from users.models import User
from reservation.models import Reservation
from notifications.models import Notification
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        reservation = Reservation.objects.get(reservation_slug=text_data_json['room_name'])

        with transaction.atomic():
            m = Message(user=User.objects.get(username=text_data_json['username']),
                        reservation=reservation,
                        content=text_data_json['message'])
            m.save()
        messages = Message.objects.filter(reservation=reservation)
        users = set()
        for mess in messages:
            users.add(mess.user)
        try:
            users.remove(m.user)
        except KeyError:
            pass
        n_description = 'New message in room {}, on reservation at {}.{}.{} at {}'.format(reservation.room.sign,
                                                                                          reservation.day_slug,
                                                                                          reservation.month_slug,
                                                                                          reservation.year_slug,
                                                                                          reservation.time)
        with transaction.atomic():
            for user in users:
                try:
                    n = Notification.objects.get(user=user,
                                                 reservation=reservation,
                                                 title='New message',
                                                 description=n_description)
                    n.is_viewed = False
                    n.datetime = datetime.now()
                except ObjectDoesNotExist:
                    n = Notification(user=user,
                                     reservation=reservation,
                                     title='New message',
                                     description=n_description,
                                     is_viewed=False)
                n.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
