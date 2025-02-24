from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
import json
from django.urls import reverse
from django.utils.safestring import mark_safe

from chat.models import ChatRoom

# Index view: Displays a list of chat rooms that the authenticated user is a member of.
# If the user is not authenticated, they are redirected to the sign-in page.
def index(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(reverse('signin_page'))

    user = request.user
    # Retrieve all chat rooms where the user is a member.
    chat_rooms = ChatRoom.objects.filter(members=user).all()

    context = {
        'chat_rooms': chat_rooms
    }
    return render(request, 'chat/index.html', context)

# Room view: Displays a specific chat room, based on the room_name.
# If the room does not exist, it is created and the current user is added.
# If the user is not authenticated, they are redirected to the sign-in page.
def room(request, room_name):
    if not request.user.is_authenticated:
        return redirect(reverse('signin_page'))

    user = request.user
    room_name = room_name.upper()
    # Check if the chat room exists, create if not.
    chat_room = ChatRoom.objects.filter(room_name=room_name)
    if not chat_room.exists():
        chat = ChatRoom.objects.create(room_name=room_name)
        chat.members.add(user)
    else:
        chat_room[0].members.add(user)

    username = request.user.username
    members_list = [
        member.username + (" (You)" if member.username == username else "") for member in chat_room[0].members.all()
    ]

    # Retrieve all chat rooms where the user is a member.
    groups = ChatRoom.objects.filter(members=user)

    context = {
        'user': user,
        'room_name': room_name,
        'groups': groups,
        'members_list': members_list,
        'username': mark_safe(json.dumps(username)),
    }
    return render(request, 'chat/room.html', context)

# Check if a chat room exists via GET request.
# If the room exists, it returns a JSON response with "exists": true; otherwise, false.
def check_chatroom(request):
    room_name = request.GET.get("room_name", "").upper()
    exists = ChatRoom.objects.filter(room_name=room_name).exists()
    return JsonResponse({
        "exists": exists
    })
