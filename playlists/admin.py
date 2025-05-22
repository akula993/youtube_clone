
from django.contrib import admin
from .models import Playlist, PlaylistVideo, PlaylistLike

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'privacy', 'created_date']
    list_filter = ['privacy', 'created_date']
    search_fields = ['title', 'creator__username']

@admin.register(PlaylistVideo)
class PlaylistVideoAdmin(admin.ModelAdmin):
    list_display = ['playlist', 'video', 'order', 'added_date']
    list_filter = ['added_date']
    search_fields = ['playlist__title', 'video__title']

@admin.register(PlaylistLike)
class PlaylistLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'playlist', 'created_date']
    list_filter = ['created_date']
