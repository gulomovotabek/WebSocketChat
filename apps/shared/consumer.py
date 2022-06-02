import json
from urllib.parse import parse_qs

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken

from core.const import ws


class WSMixin(WebsocketConsumer):
    CHANNEL_NAME = ''
    AUTH_TOKEN_CLASS = AccessToken
    TOKEN_NAME = b'token'
    user_model = get_user_model()

    def connect(self):
        self.authenticate()
        super().connect()
        async_to_sync(self.channel_layer.group_add)(self.get_group_name(), self.CHANNEL_NAME)
        if not self.check_connection_validity():
            self.close()
            return
        self.channel_add(self.CHANNEL_NAME, self.scope['user'].id, self.scope['user'], self)

    def disconnect(self, code):
        self.channel_remove(self.CHANNEL_NAME, self.scope['user'].id)
        super().disconnect(code)
        async_to_sync(self.channel_layer.group_discard)(self.get_group_name(), self.channel_name)

    def chat_message(self, event):
        sender_channel_name = event.pop('sender_channel_name')
        if self.channel_name != sender_channel_name:
            self.send(text_data=event['text'])

    def receive(self, text_data=None, bytes_data=None):
        data = self.parse_data(text_data)
        if data is None:
            return

        action = self.check_action(data)
        if action is None:
            return

        return self.socket_action(action, data.get('data'))

    def socket_action(self, action, data):
        pass

    @staticmethod
    def channel_add(scope, user_id, user, consumer):
        if scope not in ws.ALLOWED_SCOPES:
            return None

        ws.CHANNELS[scope][user_id] = {
            "user": user,
            "consumer": consumer,
        }
        return ws.CHANNELS[scope][user_id]

    @staticmethod
    def channel_remove(scope, user_id):
        try:
            return ws.CHANNELS[scope].pop(user_id)
        except Exception as e:
            print(e)

    def send_data_to_user(self, scope, user_id, text_data=None, json_data=None):
        if scope not in ws.ALLOWED_SCOPES:
            return None

        if text_data or json_data:
            if text_data:
                data = text_data
            elif json_data:
                data = json.dumps(json_data)
            else:
                print("Must pass data")
                return None
        else:
            print("Must pass data")
            return None

        if user_id not in ws.CHANNELS[scope]:
            return None

        try:
            ws.CHANNELS[scope][user_id]['consumer'].send(text_data=data)
        except Exception as e:
            print(e)
            return None

        return data

    def authenticate(self):
        try:
            validated_token = self.get_token()
            user = self.get_user(self.AUTH_TOKEN_CLASS(validated_token))
            self.scope['user'] = user
        except:
            data = {
                'success': False,
                'message': 'Token expired or invalid',
            }
            raise ValidationError(data)

    def get_token(self):
        for header in self.scope['headers']:
            if header[0] == self.TOKEN_NAME:
                return header[1]
        data = {
            'success': False,
            'message': 'token not found',
        }
        raise ValidationError(data)

    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
        except KeyError:
            data = {
                'success': False,
                'message': 'Token contained no recognizable user identification',
            }
            raise ValidationError(data)

        try:
            user = self.user_model.objects.get(id=user_id)
        except self.user_model.DoesNotExist:
            data = {
                'success': False,
                'message': 'user not found',
            }
            raise ValidationError(data)

        if not user.is_active:
            data = {
                'success': False,
                'message': 'user not found',
            }
            raise ValidationError(data)

        return user

    def get_params(self):
        get_params = parse_qs(self.scope['query_string'].decode('utf8'))
        for param in get_params:
            get_params[param] = get_params[param][0]
        return get_params

    def get_group_name(self):
        return f"consumer-{self.scope['user'].id}"

    def check_connection_validity(self):
        if not (self.scope.get('user', False) and self.scope['user'].is_authenticated):
            return False
        return True

    @staticmethod
    def get_item_by_index(items, index):
        try:
            return items[index]
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def no_action_found():
        return {
            "success": False,
            "message": {
                "ui": "Action not found",
                "dev": "Invalid action sent"
            },
            "data": {}
        }

    def parse_data(self, text_data):
        try:
            return json.loads(text_data)
        except Exception as e:
            self.send(
                text_data=json.dumps(
                    {
                        "success": False,
                        "data": None,
                        "message": {
                            "ui": "Invalid data sent",
                            "dev": "Cannot parse sent JSON",
                        }
                    }, ensure_ascii=False
                )
            )
            print(e)

    def check_action(self, data):
        if not ('action' in data and 'data' in data):
            self.send(
                text_data=json.dumps(
                    {
                        "success": False,
                        "data": None,
                        "message": {
                            "ui": "Invalid data sent",
                            "dev": "[action, data] fields are not sent",
                        }
                    }, ensure_ascii=False
                )
            )
            return
        action = data.get('action').split('.')
        if len(action) < 2:
            self.send(
                text_data=json.dumps(
                    {
                        "success": False,
                        "data": None,
                        "message": {
                            "ui": "Invalid data sent",
                            "dev": "[action] is invalid",
                        }
                    },
                    ensure_ascii=False
                )
            )
            return
        return data.get('action').split('.')
