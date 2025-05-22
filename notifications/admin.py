
from django.contrib import admin
from .models import Notification, UserPreferences

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'is_read', 'created_date']
    list_filter = ['notification_type', 'is_read', 'created_date']
    search_fields = ['recipient__username', 'message']

@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_notifications', 'push_notifications']
    search_fields = ['user__username']
