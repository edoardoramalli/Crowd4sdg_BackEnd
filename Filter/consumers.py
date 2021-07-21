from channels.generic.websocket import AsyncWebsocketConsumer

from random import randint
from time import sleep
import json


class WSConsumer(AsyncWebsocketConsumer):

    def connect(self):
        self.accept()

        for i in range(100):
            self.send(json.dumps({'message': randint(0, 5)}))
            sleep(5)

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        print('here')
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        print('Received --> ', message)
