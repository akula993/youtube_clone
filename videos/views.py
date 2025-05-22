from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.db.models import Q, F, Count  # ДОБАВИЛИ Count
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .models import Video, Category, WatchHistory
from users.models import CustomUser
from django.http import JsonResponse


class HomeListView(ListView):
    model = Video
    template_name = 'videos/home.html'
    context_object_name = 'videos'
    ordering = ['-created_date']
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class VideoDetailView(DetailView):
    model = Video

    def get(self, request, *args, **kwargs):
        video = self.get_object()
        video.views += 1
        video.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(parent=None).order_by('-created_date')
        return context


class VideoCreateView(LoginRequiredMixin, CreateView):
    model = Video
    fields = ['title', 'description', 'file', 'thumbnail', 'categories']

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)


class VideoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    fields = ['title', 'description', 'thumbnail', 'categories']

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.uploader


class VideoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    success_url = '/'

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.uploader


class UserVideoListView(ListView):
    model = Video
    template_name = 'users/user_videos.html'
    context_object_name = 'videos'
    paginate_by = 12

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.kwargs.get('username'))
        return Video.objects.filter(uploader=user).order_by('-created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, username=self.kwargs.get('username'))
        context['channel'] = user

        if self.request.user.is_authenticated:
            context['is_subscribed'] = user.subscribers.filter(id=self.request.user.id).exists()

        return context


class CategoryVideoListView(ListView):
    model = Video
    template_name = 'videos/category_videos.html'
    context_object_name = 'videos'
    paginate_by = 12

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return Video.objects.filter(categories=category).order_by('-created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        context['category'] = category
        return context


class SearchResultsView(ListView):
    model = Video
    template_name = 'videos/search_results.html'
    context_object_name = 'videos'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Video.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(uploader__username__icontains=query)
            ).order_by('-created_date')
        return Video.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['categories'] = Category.objects.all()
        return context


class TrendingVideosView(ListView):
    model = Video
    template_name = 'videos/trending.html'
    context_object_name = 'videos'
    paginate_by = 20


    def get_queryset(self):
        # Упрощенная версия - просто по просмотрам за неделю
        week_ago = timezone.now() - timedelta(days=7)
        return Video.objects.filter(
            created_date__gte=week_ago
        ).order_by('-views')

class SubscriptionsView(LoginRequiredMixin, ListView):
    model = Video
    template_name = 'videos/subscriptions.html'
    context_object_name = 'videos'
    paginate_by = 20

    def get_queryset(self):
        subscribed_users = self.request.user.subscribed_to.all()
        return Video.objects.filter(
            uploader__in=subscribed_users
        ).order_by('-created_date')


class HistoryView(LoginRequiredMixin, ListView):
    model = WatchHistory
    template_name = 'videos/history.html'
    context_object_name = 'history_items'
    paginate_by = 20

    def get_queryset(self):
        return WatchHistory.objects.filter(
            user=self.request.user
        ).select_related('video', 'video__uploader').order_by('-watched_at')


class LikedVideosView(LoginRequiredMixin, ListView):
    model = Video
    template_name = 'videos/liked_videos.html'
    context_object_name = 'videos'
    paginate_by = 20

    def get_queryset(self):
        return self.request.user.liked_videos.all().order_by('-created_date')


@login_required
def like_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
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
        'likes': video.get_like_count(),
        'dislikes': video.get_dislike_count(),
        'liked': liked
    })


@login_required
def dislike_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
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
        'likes': video.get_like_count(),
        'dislikes': video.get_dislike_count(),
        'disliked': disliked
    })


@login_required
def subscribe_to_channel(request, pk):
    channel = get_object_or_404(CustomUser, pk=pk)
    user = request.user

    if channel == user:
        return JsonResponse({'error': 'Вы не можете подписаться на себя'}, status=400)

    if user in channel.subscribers.all():
        channel.subscribers.remove(user)
        subscribed = False
    else:
        channel.subscribers.add(user)
        subscribed = True

    return JsonResponse({
        'subscribers': channel.subscribers.count(),
        'subscribed': subscribed
    })
