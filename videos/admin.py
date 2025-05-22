from django.contrib import admin
from .models import Video, Category

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploader', 'views', 'created_date']
    list_filter = ['created_date', 'categories', 'uploader']
    search_fields = ['title', 'description', 'uploader__username']
    readonly_fields = ['views', 'created_date']
    filter_horizontal = ['categories', 'likes', 'dislikes']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
