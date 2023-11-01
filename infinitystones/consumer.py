import datetime
import json
import time

from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

from infinitystones.models import Activation


class StoneActivationStatus(WebsocketConsumer):
    def connect(self):
        print("connect")
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        username = data['username']

        ret_val = {}

        try:
            user = User.objects.get(username=username)

            # query the db every 10 seconds until the client closes the connection or until 10 minutes
            # for now, we rely on client to close the connection after all activation requests are complete

            end_time = datetime.datetime.now() + datetime.timedelta(seconds=600)

            while datetime.datetime.now() < end_time:
                non_terminal_activations = Activation.objects.filter(user=user, status__in=['A', 'B'])

                if not non_terminal_activations:
                    self.send(json.dumps({"data": []}))
                else:
                    data = []
                    for activation in non_terminal_activations:
                        data.append({
                            "id": activation.id,
                            "status": activation.status,
                            "end_time": activation.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                            "duration": activation.duration
                        })

                    self.send(json.dumps({"data": data}))
                time.sleep(10)

        except User.DoesNotExist:
            ret_val = {"comment": "user doesn't exist for username: " + username}

        self.send(text_data=json.dumps(ret_val))
