from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter, ProtocolTypeRouter
from django.urls import path
from .consumers import EchoConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path(r"ws/<slug:name>/<slug:namespace>", EchoConsumer),
        ])
    )
})