from django.contrib import admin

from .models import Conversation, InboxMessage


admin.site.register(Conversation)
admin.site.register(InboxMessage)
