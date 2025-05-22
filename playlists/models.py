from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import CustomUser
from videos.models import Video


class Playlist(models.Model):
    PRIVACY_CHOICES = [
        ('public', 'Публичный'),
        ('unlisted', 'По ссылке'),
        ('private', 'Приватный'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='playlists')
    videos = models.ManyToManyField(Video, through='PlaylistVideo', related_name='in_playlists')
    thumbnail = models.ImageField(upload_to='playlist_thumbnails', blank=True, null=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('playlist-detail', kwargs={'pk': self.pk})

    def get_video_count(self):
        return self.videos.count()

    def get_duration(self):
        # Здесь можно посчитать общую длительность плейлиста
        return "1:23:45"  # Placeholder

    def get_first_video(self):
        playlist_video = self.playlistvideo_set.first()
        return playlist_video.video if playlist_video else None


class PlaylistVideo(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    added_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['order']
        unique_together = ['playlist', 'video']


class PlaylistLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['user', 'playlist']
