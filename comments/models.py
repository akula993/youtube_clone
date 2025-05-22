from django.db import models
from django.utils import timezone
from users.models import CustomUser
from videos.models import Video


class Comment(models.Model):
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes = models.ManyToManyField(CustomUser, related_name='liked_comments', blank=True)
    dislikes = models.ManyToManyField(CustomUser, related_name='disliked_comments', blank=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.video.title}'

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Коментарий'
        verbose_name_plural = "Коментарии"
        db_table = 'comments'

