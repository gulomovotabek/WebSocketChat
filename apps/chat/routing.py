from django.urls import path

from chat.ws.consumer import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat', ChatConsumer.as_asgi()),
]
