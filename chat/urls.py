from django.urls import path, re_path
from .views import room, index, check_chatroom

# URL patterns for routing various requests to appropriate views.
urlpatterns = [
    # Index page: The landing page for the chat application.
    path('', index, name="index_page"),

    # Room page: A dynamic URL that captures the room name from the URL and displays a specific chat room.
    # The room_name is passed as a parameter to the room view.
    re_path(r'^(?P<room_name>[\w-]+)/$', room, name="room_page"),

    # Check Room page: A page to check if a chat room exists.
    # This view used for validating or creating rooms.
    path("check/check-room/", check_chatroom, name="check_room"),
]
