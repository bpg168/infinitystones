import datetime
import json
import threading
import time

import pytz
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

from infinitystones.models import Activation


class StoneActivationStatus(WebsocketConsumer):

    power_status_thread = None
    is_channel_open = False

    def connect(self):
        print(f"accepting websocket connection, client side port: {self.scope['client'][1]}")
        self.accept()

    def disconnect(self, close_code):
        self.is_channel_open = False
        print(f"disconnecting the channel with close_code: {close_code}, client side port: {self.scope['client'][1]}")

    def receive(self, text_data):
        data = json.loads(text_data)
        username = data.get('username')

        if not username:
            self.send("`username` cannot be empty")
            return

        try:
            user = User.objects.get(username=username)
            self.is_channel_open = True
            self.power_status_thread = threading.Thread(target=self.send_task_status, args=(user, ))
            self.power_status_thread.start()
        except User.DoesNotExist:
            self.send(f"username doesn't exist: {username}")

    def send_task_status(self, user: User):
        while self.is_channel_open:
            non_terminal_activations = Activation.objects.filter(user=user, status__in=['A', 'B'])
            data = []

            if not non_terminal_activations:
                self.send(json.dumps({"data": []}))
                continue

            for activation in non_terminal_activations:
                data.append({
                    "id": activation.id,
                    "status": activation.status,
                    "end_time": activation.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "remaining_duration": round(
                        (activation.end_time - datetime.datetime.now(tz=pytz.UTC)).total_seconds()
                    )
                })

            self.send(json.dumps({"data": data}))

            print(f"notification sent to client side port: [{self.scope['client'][1]}], sending notification again in 2 seconds")
            time.sleep(2)
