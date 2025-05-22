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

    if user in comment.likes.all():
        comment.likes.remove(user)
        liked = False
    else:
        if user in comment.dislikes.all():
            comment.dislikes.remove(user)
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

    if user in comment.dislikes.all():
        comment.dislikes.remove(user)
        disliked = False
    else:
        if user in comment.likes.all():
            comment.likes.remove(user)
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

    if request.user == comment.author or request.user == comment.video.uploader:
        comment.delete()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})

    return redirect('video-detail', pk=video_id)
