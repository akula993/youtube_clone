
from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'video', 'created_date', 'parent']
    list_filter = ['created_date', 'video']
    search_fields = ['content', 'author__username', 'video__title']
    raw_id_fields = ['parent']
