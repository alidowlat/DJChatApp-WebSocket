from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()


class ChatRoom(models.Model):
    # Room name for chat (maximum length 50 characters). The name will be stripped of extra spaces and spaces within
    # will be replaced by underscores and converted to uppercase before saving.
    room_name = models.CharField(max_length=50, blank=True)

    # Members of the chat room. Many-to-many relation with User model.
    members = models.ManyToManyField(user)

    def __str__(self):
        # Return the room name when the object is printed
        return self.room_name

    def save(self, *args, **kwargs):
        # Clean the room name by stripping, replacing spaces with underscores, and converting to uppercase
        self.room_name = self.room_name.strip().replace(" ", "_").upper()
        super().save(*args, **kwargs)

    class Meta:
        # Defining the plural name and database table for the model
        verbose_name = 'Chat Room'
        verbose_name_plural = 'Chat Rooms'
        db_table = 'c_chatrooms'


class Message(models.Model):
    # ForeignKey relationship to the User model representing the sender of the message
    sender = models.ForeignKey(user, on_delete=models.CASCADE)

    # ForeignKey relationship to the ChatRoom model representing the room where the message was sent
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True)

    # The actual message content
    message = models.TextField()

    # The date and time when the message was sent. Automatically set when the message is created.
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Return the sender's username when the object is printed
        return self.sender.username

    def last_message(self, room_name):
        # Fetch the last message(s) in the given chat room ordered by date
        return Message.objects.filter(chat_room__room_name=room_name).order_by('date').all()

    class Meta:
        # Defining the plural name and database table for the model
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        db_table = 'c_messages'
