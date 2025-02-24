from rest_framework import serializers
from .models import Message

# Serializer for the Message model to control how Message instances are converted to JSON format.
# Fields:
# - '__str__' - The string representation of the message's sender (user's username).
# - 'message' - The text content of the message.
# - 'date' - The timestamp when the message was sent.
class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['__str__', 'message', 'date']
