from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from cli import consumers

websocket_urlpatterns = [
    path('ws/search/', consumers.UsernameSearchConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": URLRouter(websocket_urlpatterns),
})
