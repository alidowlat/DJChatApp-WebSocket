from django.contrib import admin
from . import models


class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'date']
    list_filter = ['date']


admin.site.register(models.Message, MessageAdmin)
admin.site.register(models.ChatRoom)
