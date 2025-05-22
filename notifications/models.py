from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import CustomUser
from videos.models import Video


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('new_video', 'Новое видео'),
        ('new_subscriber', 'Новый подписчик'),
        ('video_like', 'Лайк видео'),
        ('comment', 'Комментарий'),
        ('comment_reply', 'Ответ на комментарий'),
        ('playlist_add', 'Добавление в плейлист'),
        ('mention', 'Упоминание'),
    ]

    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_notifications')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_notifications', null=True,
                               blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f'{self.get_notification_type_display()} для {self.recipient.username}'

    def get_absolute_url(self):
        if self.video:
            return reverse('video-detail', kwargs={'pk': self.video.pk})
        elif self.sender:
            return reverse('user-videos', kwargs={'username': self.sender.username})
        return reverse('home')


class UserPreferences(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='notification_preferences')
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    new_video_notifications = models.BooleanField(default=True)
    comment_notifications = models.BooleanField(default=True)
    like_notifications = models.BooleanField(default=False)

    def __str__(self):
        return f'Настройки {self.user.username}'

