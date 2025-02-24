import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import QuerySet

from .serializers import MessageSerializers
from .models import Message, ChatRoom
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user_model

user = get_user_model()


class ChatConsumer(WebsocketConsumer):
    """
    A WebSocket consumer that handles real-time chat functionality within chat rooms.

    It provides the following methods:
    - new_message: Handles sending new messages in the chat room.
    - notification: Sends notifications to chat room members when a new message is received.
    - fetch_message: Retrieves and sends previous messages from the chat room.
    - image: Handles sending image data in the chat room.
    - message_serializer: Serializes message data into JSON format.
    - connect: Manages the WebSocket connection and subscribes to the chat room.
    - disconnect: Manages disconnection and removes the user from the chat room.
    - receive: Processes incoming WebSocket messages.
    - send_to_chat_message: Sends messages to all members of the chat room.
    - chat_message: Sends messages from the room group to the WebSocket client.
    """

    def new_message(self, data):
        """
        Handles new incoming messages.

        Args:
            data (dict): Contains message data including 'username', 'message', and 'room_name'.

        The method creates a new message instance, saves it to the database, and sends it to the chat room.
        """
        sender = data['username']
        message = data['message']
        room_name = data['room_name']

        # Notify chat room members about the new message
        self.notification(data)

        # Create a new chat room instance
        chat_room = ChatRoom.objects.get(room_name=room_name)

        # Fetch the user from the database
        user_model = user.objects.filter(username=sender).first()

        # Create a new message instance
        message_instance = Message.objects.create(sender=user_model, message=message, chat_room=chat_room)

        # Serialize the message instance
        result = eval(self.message_serializer(message_instance))

        # Send the serialized message to the chat room
        self.send_to_chat_message(result)

    def notification(self, data):
        """
        Sends a notification to all members of the chat room when a new message is received.

        Args:
            data (dict): Contains message data including 'username', 'message', and 'room_name'.

        The method notifies all members of the chat room by broadcasting a message to the WebSocket.
        """
        message_chatroom = data['room_name']
        chat_room_qs = ChatRoom.objects.filter(room_name=message_chatroom)
        members_list = [member.username for member in chat_room_qs[0].members.all()]

        async_to_sync(self.channel_layer.group_send)(
            'chat_listener', {
                "type": "chat_message",
                "message": data['message'],
                "__str__": data['username'],
                "room_name": message_chatroom,
                'members_list': members_list
            }
        )

    def fetch_message(self, data):
        """
        Fetches and sends previous messages from the chat room.

        Args:
            data (dict): Contains the 'room_name' for which previous messages should be fetched.

        This method retrieves the last messages from the database for the specified chat room and sends them to the WebSocket.
        """
        room_name = data["room_name"]

        # Get the last messages from the database for the room
        queryset = Message.last_message(self, room_name=room_name)

        # Serialize the messages
        message_json = self.message_serializer(queryset)

        # Create context to send the fetched messages
        context = {
            'message': eval(message_json),
            'command': 'fetch_message',
        }

        # Send the fetched messages to the WebSocket
        self.chat_message(context)

    def image(self, data):
        """
        Handles image messages.

        Args:
            data (dict): Contains the image data to be sent.

        This method sends image data to the chat room through WebSocket.
        """
        self.send_to_chat_message(data)

    def message_serializer(self, queryset):
        """
        Serializes a queryset of Message objects into JSON.

        Args:
            queryset (QuerySet or Message): The message data to be serialized.

        Returns:
            str: The serialized JSON string of the messages.

        This method serializes the queryset of messages or a single message into JSON format.
        """
        many = isinstance(queryset, QuerySet)
        serialized = MessageSerializers(queryset, many=many)
        return JSONRenderer().render(serialized.data).decode('utf-8')

    def connect(self):
        """
        Manages the WebSocket connection and subscribes to the specified chat room group.

        This method adds the WebSocket connection to the group representing the chat room.
        """
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        """
        Manages disconnection and removes the WebSocket from the chat room group.

        Args:
            close_code (int): The code that indicates why the connection was closed.

        This method removes the WebSocket connection from the chat room group and ends the connection.
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        """
        Processes incoming WebSocket messages.

        Args:
            text_data (str): The message received from the WebSocket.

        The method identifies the type of message (command) and calls the corresponding handler.
        """
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        self.commands[command](self, text_data_json)

    def send_to_chat_message(self, message):
        """
        Sends a message to the WebSocket group representing the chat room.

        Args:
            message (dict): The message to be sent to the chat room group.

        This method broadcasts the message to all members in the specified chat room.
        """
        command = message.get("command", None)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat_message",
                "message": message['message'],
                "date": message.get('date', ''),
                "command": (lambda command: "img" if (command == "img") else "new_message")(command),
                "__str__": message['__str__'],
            }
        )

    def chat_message(self, event):
        """
        Sends a chat message to the WebSocket.

        Args:
            event (dict): The event that contains the message data to be sent to the WebSocket.

        This method sends the received message to the WebSocket client.
        """
        self.send(text_data=json.dumps(event))

    # Mapping commands to methods
    commands = {
        'new_message': new_message,
        'fetch_message': fetch_message,
        'img': image
    }
