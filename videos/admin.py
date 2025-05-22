
from django.contrib import admin
from .models import Video, Category, WatchHistory, VideoRecommendation

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

@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'watched_at', 'watch_duration']
    list_filter = ['watched_at']
    search_fields = ['user__username', 'video__title']

@admin.register(VideoRecommendation)
class VideoRecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'score', 'reason', 'created_date']
    list_filter = ['reason', 'created_date']
    search_fields = ['user__username', 'video__title']
