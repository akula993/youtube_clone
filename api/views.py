from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from videos.models import Video


@login_required
@require_POST
def clear_history_api(request):
    """Очистить историю просмотров"""
    from videos.models import WatchHistory
    WatchHistory.objects.filter(user=request.user).delete()
    return JsonResponse({'success': True})


def search_videos_api(request):
    """Поиск видео для API"""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'videos': []})

    videos = Video.objects.filter(title__icontains=query)[:10]

    video_data = []
    for video in videos:
        video_data.append({
            'id': video.id,
            'title': video.title,
            'thumbnail': video.thumbnail.url,
            'uploader': video.uploader.username,
        })

    return JsonResponse({'videos': video_data})
