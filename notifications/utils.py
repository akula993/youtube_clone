from django.shortcuts import get_object_or_404
from .models import Notification, UserPreferences
from videos.models import Video
from users.models import CustomUser


class NotificationService:
    @staticmethod
    def create_notification(recipient, notification_type, message, sender=None, video=None):
        """Создать уведомление"""
        # Проверяем настройки пользователя
        try:
            preferences = recipient.notification_preferences
        except UserPreferences.DoesNotExist:
            preferences = UserPreferences.objects.create(user=recipient)

        # Проверяем, включены ли уведомления данного типа
        should_notify = True
        if notification_type == 'new_video' and not preferences.new_video_notifications:
            should_notify = False
        elif notification_type in ['comment', 'comment_reply'] and not preferences.comment_notifications:
            should_notify = False
        elif notification_type == 'video_like' and not preferences.like_notifications:
            should_notify = False

        if should_notify:
            return Notification.objects.create(
                recipient=recipient,
                sender=sender,
                notification_type=notification_type,
                message=message,
                video=video
            )
        return None

    @staticmethod
    def notify_new_video(video):
        """Уведомить подписчиков о новом видео"""
        subscribers = video.uploader.subscribers.all()

        for subscriber in subscribers:
            NotificationService.create_notification(
                recipient=subscriber,
                sender=video.uploader,
                notification_type='new_video',
                message=f'{video.uploader.username} опубликовал новое видео: "{video.title}"',
                video=video
            )

    @staticmethod
    def notify_new_subscriber(channel_owner, new_subscriber):
        """Уведомить о новом подписчике"""
        NotificationService.create_notification(
            recipient=channel_owner,
            sender=new_subscriber,
            notification_type='new_subscriber',
            message=f'{new_subscriber.username} подписался на ваш канал'
        )

    @staticmethod
    def notify_video_like(video, user):
        """Уведомить о лайке видео"""
        if video.uploader != user:  # Не уведомляем автора о собственных лайках
            NotificationService.create_notification(
                recipient=video.uploader,
                sender=user,
                notification_type='video_like',
                message=f'{user.username} оценил ваше видео: "{video.title}"',
                video=video
            )

    @staticmethod
    def notify_comment(comment):
        """Уведомить о новом комментарии"""
        if comment.video.uploader != comment.author:
            NotificationService.create_notification(
                recipient=comment.video.uploader,
                sender=comment.author,
                notification_type='comment',
                message=f'{comment.author.username} прокомментировал ваше видео: "{comment.video.title}"',
                video=comment.video
            )

    @staticmethod
    def notify_comment_reply(reply):
        """Уведомить об ответе на комментарий"""
        if reply.parent and reply.parent.author != reply.author:
            NotificationService.create_notification(
                recipient=reply.parent.author,
                sender=reply.author,
                notification_type='comment_reply',
                message=f'{reply.author.username} ответил на ваш комментарий',
                video=reply.video
            )
