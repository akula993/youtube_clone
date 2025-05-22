from django.db.models import Count, Q, F
from videos.models import Video, WatchHistory, VideoRecommendation
from users.models import CustomUser
import random
from collections import defaultdict


class RecommendationEngine:
    def __init__(self, user):
        self.user = user

    def get_recommendations(self, limit=20):
        """Получить рекомендации для пользователя"""
        if not self.user.is_authenticated:
            return self.get_trending_videos(limit)

        recommendations = []

        # 1. На основе истории просмотров
        history_recs = self.get_history_based_recommendations(limit // 4)
        recommendations.extend(history_recs)

        # 2. На основе лайков
        like_recs = self.get_like_based_recommendations(limit // 4)
        recommendations.extend(like_recs)

        # 3. На основе подписок
        subscription_recs = self.get_subscription_based_recommendations(limit // 4)
        recommendations.extend(subscription_recs)

        # 4. Популярные видео
        trending_recs = self.get_trending_videos(limit // 4)
        recommendations.extend(trending_recs)

        # Убираем дубликаты и перемешиваем
        seen_ids = set()
        unique_recs = []
        for video in recommendations:
            if video.id not in seen_ids:
                seen_ids.add(video.id)
                unique_recs.append(video)

        random.shuffle(unique_recs)
        return unique_recs[:limit]

    def get_history_based_recommendations(self, limit=5):
        """Рекомендации на основе истории просмотров"""
        # Получаем категории из истории просмотров
        watched_categories = WatchHistory.objects.filter(
            user=self.user
        ).values_list('video__categories', flat=True)

        if not watched_categories:
            return []

        # Исключаем уже просмотренные видео
        watched_video_ids = WatchHistory.objects.filter(
            user=self.user
        ).values_list('video_id', flat=True)

        return Video.objects.filter(
            categories__in=watched_categories
        ).exclude(
            id__in=watched_video_ids
        ).exclude(
            uploader=self.user
        ).annotate(
            views_count=F('views')
        ).order_by('-views_count')[:limit]

    def get_like_based_recommendations(self, limit=5):
        """Рекомендации на основе лайков"""
        liked_categories = self.user.liked_videos.values_list('categories', flat=True)

        if not liked_categories:
            return []

        liked_video_ids = self.user.liked_videos.values_list('id', flat=True)

        return Video.objects.filter(
            categories__in=liked_categories
        ).exclude(
            id__in=liked_video_ids
        ).exclude(
            uploader=self.user
        ).order_by('-views', '-created_date')[:limit]

    def get_subscription_based_recommendations(self, limit=5):
        """Рекомендации на основе подписок"""
        subscribed_users = self.user.subscribed_to.all()

        if not subscribed_users:
            return []

        return Video.objects.filter(
            uploader__in=subscribed_users
        ).order_by('-created_date')[:limit]

    def get_trending_videos(self, limit=5):
        """Популярные видео"""
        return Video.objects.annotate(
            engagement_score=F('views') + F('likes__count') * 10
        ).order_by('-engagement_score', '-created_date')[:limit]

    def update_recommendations(self):
        """Обновить рекомендации для пользователя"""
        if not self.user.is_authenticated:
            return

        # Удаляем старые рекомендации
        VideoRecommendation.objects.filter(user=self.user).delete()

        # Создаем новые рекомендации
        recommendations = self.get
