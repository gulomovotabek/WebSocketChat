from channels import routing
from django.core.asgi import get_asgi_application

from chat.routing import websocket_urlpatterns

application = routing.ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": routing.URLRouter(websocket_urlpatterns),
})
