from django.urls import re_path
from .consumers import ChatConsumer

# URL pattern for WebSocket connection.
# This will match any URL that starts with 'ws/chat/' followed by a room name (only alphanumeric characters and underscores allowed).
# The room name is captured and passed to the ChatConsumer as part of the WebSocket URL.
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]
