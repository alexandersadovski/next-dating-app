from django.contrib import admin
from next.dashboard.models import UserInteraction


@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_user', 'liked')
    list_filter = ('liked',)
    search_fields = ('user__email', 'target_user__email')
    ordering = ('user__email',)
