from django.contrib import admin
from next.messaging.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('sender__email', 'receiver__email', 'content')
    ordering = ('-timestamp',)
