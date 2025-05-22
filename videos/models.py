from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = "Категория"
        db_table = 'category'


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='videos')
    thumbnail = models.ImageField(upload_to='thumbnails', default='default_thumbnail.jpg')
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='videos')
    views = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField(Category, related_name='videos', blank=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_videos', blank=True)
    dislikes = models.ManyToManyField(CustomUser, related_name='disliked_videos', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('video-detail', kwargs={'pk': self.pk})

    def get_like_count(self):
        return self.likes.count()

    def get_dislike_count(self):
        return self.dislikes.count()

    class Meta:
        verbose_name_plural = "Видео"
        verbose_name = "Видео"
        db_table = 'video'
