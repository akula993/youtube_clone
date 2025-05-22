from django.urls import path
from . import views

urlpatterns = [
    # Поиск и рекомендации
    path('search-videos/', views.search_videos_api, name='api-search-videos'),
    path('search-suggestions/', views.search_suggestions_api, name='api-search-suggestions'),
    path('recommendations/', views.recommendations_api, name='api-recommendations'),
    path('update-recommendations/', views.update_recommendations_api, name='api-update-recommendations'),

    # Взаимодействие с видео
    path('video/<int:video_id>/like/', views.like_video_api, name='api-like-video'),
    path('video/<int:video_id>/dislike/', views.dislike_video_api, name='api-dislike-video'),
    path('add-to-history/<int:video_id>/', views.add_to_history_api, name='api-add-to-history'),
    path('update-watch-duration/<int:video_id>/', views.update_watch_duration_api, name='api-update-watch-duration'),

    # Комментарии
    path('comments/<int:video_id>/', views.comments_api, name='api-comments'),

    # Уведомления
    path('notifications/unread-count/', views.unread_notifications_count_api, name='api-unread-notifications'),

    # Аналитика
    path('analytics/track/', views.track_event_api, name='api-track-event'),
]
