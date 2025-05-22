from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from .models import Playlist, PlaylistVideo
from videos.models import Video
import json


class PlaylistListView(LoginRequiredMixin, ListView):
    model = Playlist
    template_name = 'playlists/playlist_list.html'
    context_object_name = 'playlists'
    paginate_by = 12

    def get_queryset(self):
        return Playlist.objects.filter(creator=self.request.user).order_by('-updated_date')


class PlaylistDetailView(DetailView):
    model = Playlist
    template_name = 'playlists/playlist_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        playlist = self.get_object()

        # Проверка доступа к плейлисту
        if playlist.privacy == 'private' and playlist.creator != self.request.user:
            return redirect('playlist-list')

        context['playlist_videos'] = PlaylistVideo.objects.filter(
            playlist=playlist
        ).select_related('video', 'video__uploader').order_by('order')

        return context


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    template_name = 'playlists/playlist_form.html'
    fields = ['title', 'description', 'privacy']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class PlaylistUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Playlist
    template_name = 'playlists/playlist_form.html'
    fields = ['title', 'description', 'privacy']

    def test_func(self):
        playlist = self.get_object()
        return self.request.user == playlist.creator


class PlaylistDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Playlist
    template_name = 'playlists/playlist_confirm_delete.html'
    success_url = reverse_lazy('playlist-list')

    def test_func(self):
        playlist = self.get_object()
        return self.request.user == playlist.creator


@login_required
def add_to_playlist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        video_id = data.get('video_id')
        playlist_id = data.get('playlist_id')

        video = get_object_or_404(Video, id=video_id)
        playlist = get_object_or_404(Playlist, id=playlist_id, creator=request.user)

        # Проверяем, не добавлено ли уже видео в плейлист
        if not PlaylistVideo.objects.filter(playlist=playlist, video=video).exists():
            # Получаем максимальный порядок и добавляем видео в конец
            max_order = PlaylistVideo.objects.filter(playlist=playlist).aggregate(
                max_order=models.Max('order')
            )['max_order'] or 0

            PlaylistVideo.objects.create(
                playlist=playlist,
                video=video,
                order=max_order + 1
            )

            return JsonResponse({'success': True, 'message': 'Видео добавлено в плейлист'})
        else:
            return JsonResponse({'success': False, 'message': 'Видео уже в плейлисте'})

    return JsonResponse({'success': False, 'message': 'Неверный запрос'})


@login_required
def remove_from_playlist(request, playlist_id, video_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, creator=request.user)
    video = get_object_or_404(Video, id=video_id)

    playlist_video = get_object_or_404(PlaylistVideo, playlist=playlist, video=video)
    playlist_video.delete()

    # Переупорядочиваем оставшиеся видео
    remaining_videos = PlaylistVideo.objects.filter(playlist=playlist).order_by('order')
    for i, pv in enumerate(remaining_videos):
        pv.order = i + 1
        pv.save()

    messages.success(request, 'Видео удалено из плейлиста')
    return redirect('playlist-detail', pk=playlist_id)


@login_required
def reorder_playlist(request, playlist_id):
    if request.method == 'POST':
        playlist = get_object_or_404(Playlist, id=playlist_id, creator=request.user)
        data = json.loads(request.body)
        video_orders = data.get('video_orders', [])

        for item in video_orders:
            video_id = item['video_id']
            new_order = item['order']

            try:
                playlist_video = PlaylistVideo.objects.get(
                    playlist=playlist,
                    video_id=video_id
                )
                playlist_video.order = new_order
                playlist_video.save()
            except PlaylistVideo.DoesNotExist:
                continue

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


@login_required
def get_user_playlists(request, video_id):
    """Получить плейлисты пользователя для добавления видео"""
    video = get_object_or_404(Video, id=video_id)
    playlists = Playlist.objects.filter(creator=request.user)

    playlist_data = []
    for playlist in playlists:
        is_in_playlist = PlaylistVideo.objects.filter(
            playlist=playlist,
            video=video
        ).exists()

        playlist_data.append({
            'id': playlist.id,
            'title': playlist.title,
            'video_count': playlist.get_video_count(),
            'is_in_playlist': is_in_playlist
        })

    return JsonResponse({'playlists': playlist_data})
