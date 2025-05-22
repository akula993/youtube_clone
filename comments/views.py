from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Comment
from videos.models import Video


@login_required
def create_comment(request, video_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        video = get_object_or_404(Video, id=video_id)

        if content:
            comment = Comment.objects.create(
                content=content,
                author=request.user,
                video=video
            )

            # Если запрос AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'id': comment.id,
                    'content': comment.content,
                    'author': comment.author.username,
                    'created_date': comment.created_date.strftime('%d.%m.%Y %H:%M'),
                    'likes': 0,
                    'dislikes': 0
                })

            return redirect('video-detail', pk=video_id)

    return redirect('video-detail', pk=video_id)


@login_required
def reply_comment(request, comment_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        parent_comment = get_object_or_404(Comment, id=comment_id)

        if content:
            reply = Comment.objects.create(
                content=content,
                author=request.user,
                video=parent_comment.video,
                parent=parent_comment
            )

            # Если запрос AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'id': reply.id,
                    'content': reply.content,
                    'author': reply.author.username,
                    'created_date': reply.created_date.strftime('%d.%m.%Y %H:%M'),
                    'likes': 0,
                    'dislikes': 0
                })

            return redirect('video-detail', pk=parent_comment.video.id)

    return redirect('video-detail', pk=parent_comment.video.id)


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    # Если пользователь уже лайкнул, то убираем лайк
    if user in comment.likes.all():
        comment.likes.remove(user)
        liked = False
    else:
        # Убираем дизлайк, если есть
        if user in comment.dislikes.all():
            comment.dislikes.remove(user)
        # Добавляем лайк
        comment.likes.add(user)
        liked = True

    return JsonResponse({
        'likes': comment.likes.count(),
        'dislikes': comment.dislikes.count(),
        'liked': liked
    })


@login_required
def dislike_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    # Если пользователь уже дизлайкнул, то убираем дизлайк
    if user in comment.dislikes.all():
        comment.dislikes.remove(user)
        disliked = False
    else:
        # Убираем лайк, если есть
        if user in comment.likes.all():
            comment.likes.remove(user)
        # Добавляем дизлайк
        comment.dislikes.add(user)
        disliked = True

    return JsonResponse({
        'likes': comment.likes.count(),
        'dislikes': comment.dislikes.count(),
        'disliked': disliked
    })


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    video_id = comment.video.id

    # Только автор или владелец видео может удалить комментарий
    if request.user == comment.author or request.user == comment.video.uploader:
        comment.delete()

        # Если запрос AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})

    return redirect('video-detail', pk=video_id)


# В файле views.py можно добавить систему рекомендаций
def get_recommended_videos(user, current_video=None):
    if user.is_authenticated:
        # Рекомендации на основе лайков и просмотров пользователя
        liked_categories = user.liked_videos.values_list('categories', flat=True)
        recommended = Video.objects.filter(
            categories__in=liked_categories
        ).exclude(id=current_video.id if current_video else None)
    else:
        # Популярные видео для неавторизованных пользователей
        recommended = Video.objects.all().order_by('-views')

    return recommended[:10]
