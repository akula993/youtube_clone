from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'date_joined', 'is_staff']
    list_filter = ['date_joined', 'is_staff', 'is_active']
    search_fields = ['username', 'email']

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('profile_picture', 'bio', 'website', 'subscribers')
        }),
    )

    filter_horizontal = ['subscribers']
