from django.contrib import admin
from next.accounts.models import AppUser, Profile


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.readonly_fields + ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')
        return self.readonly_fields

    def has_change_permission(self, request, obj=None):
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'age', 'gender')
    list_filter = ('gender', 'age')
    search_fields = ('first_name', 'last_name', 'user__email')
    ordering = ('user__email',)
