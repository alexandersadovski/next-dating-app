from django.contrib import admin
from next.matches.models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user1__email', 'user2__email')
    ordering = ('-created_at',)
