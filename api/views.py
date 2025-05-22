from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from videos.models import Video, WatchHistory
from comments.models import Comment
from notifications.models import Notification
from recommendations.utils import RecommendationEngine
import json


@login_required
def search_videos_api(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'videos': []})

    videos = Video.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(uploader__username__icontains=query)
    )[:10]

    video_data = []
    for video in videos:
        video_data.append({
            'id': video.id,
            'title': video.title,
            'thumbnail': video.thumbnail.url,
            'uploader': video.uploader.username,
            'views': video.views,
            'duration': '5:30'  # Placeholder
        })

    return JsonResponse({'videos': video_data})


def search_suggestions_api(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'suggestions': []})

    # Здесь можно добавить логику для автодополнения
    suggestions = [
        {'text': f'{query} tutorial'},
        {'text': f'{query} review'},
        {'text': f'{query} guide'},
    ]

    return JsonResponse({'suggestions': suggestions})


@login_required
def recommendations_api(request):
    page = int(request.GET.get('page', 1))
    engine = RecommendationEngine(request.user)
    videos = engine.get_recommendations(20)

    video_data = []
    for video in videos:
        video_data.append({
            'id': video.id,
            'title': video.title,
            'thumbnail': video.thumbnail.url,
            'uploader': {
                'username': video.uploader.username,
                'avatar': video.uploader.profile_picture.url
            },
            'views': video.views,
            'duration': '5:30',  # Placeholder
            'created_ago': '2 дня назад'  # Placeholder
        })

    return JsonResponse({'videos': video_data})


@login_required
@require_POST
def update_recommendations_api(request):
    engine = RecommendationEngine(request.user)
    engine.update_recommendations()
    return JsonResponse({'success': True})


@login_required
@require_POST
def like_video_api(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    user = request.user

    if user in video.likes.all():
        video.likes.remove(user)
        liked = False
    else:
        if user in video.dislikes.all():
            video.dislikes.remove(user)
        video.likes.add(user)
        liked = True

    return JsonResponse({
        'success': True,
        'liked': liked,
        'likes': video.likes.count(),
        'dislikes': video.dislikes.count()
    })


@login_required
@require_POST
def dislike_video_api(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    user = request.user

    if user in video.dislikes.all():
        video.dislikes.remove(user)
        disliked = False
    else:
        if user in video.likes.all():
            video.likes.remove(user)
        video.dislikes.add(user)
        disliked = True

    return JsonResponse({
        'success': True,
        'disliked': disliked,
        'likes': video.likes.count(),
        'dislikes': video.dislikes.count()
    })


@login_required
@require_POST
def add_to_history_api(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    history_item, created = WatchHistory.objects.get_or_create(
        user=request.user,
        video=video
    )

    if not created:
        history_item.watched_at = timezone.now()
        history_item.save()

    return JsonResponse({'success': True})


@login_required
@require_POST
def update_watch_duration_api(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    duration = int(request.POST.get('duration', 0))

    history_item, created = WatchHistory.objects.get_or_create(
        user=request.user,
        video=video
    )

    history_item.watch_duration = max(history_item.watch_duration, duration)
    history_item.save()

    return JsonResponse({'success': True})


def comments_api(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    page = int(request.GET.get('page', 1))

    comments = Comment.objects.filter(
        video=video,
        parent=None
    ).select_related('author').order_by('-created_date')

    # Простая пагинация
    start = (page - 1) * 10
    end = start + 10
    page_comments = comments[start:end]

    comment_data = []
    for comment in page_comments:
        comment_data.append({
            'id': comment.id,
            'content': comment.content,
            'author': {
                'username': comment.author.username,
                'avatar': comment.author.profile_picture.url
            },
            'likes': comment.likes.count(),
            'dislikes': comment.dislikes.count(),
            'created_ago': '2 часа назад'  # Placeholder
        })

    return JsonResponse({'comments': comment_data})


@login_required
def unread_notifications_count_api(request):
    count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()

    return JsonResponse({'count': count})


@login_required
@require_POST
def track_event_api(request):
    event_type = request.POST.get('event_type')
    video_id = request.POST.get('video_id')
    data = request.POST.get('data', '{}')

    # Здесь можно добавить логику для сохранения аналитики
    # Например, в модель Analytics или отправить в внешний сервис

    return JsonResponse({'success': True})
