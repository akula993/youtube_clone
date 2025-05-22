from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('video/<int:pk>/', views.VideoDetailView.as_view(), name='video-detail'),
    path('video/new/', views.VideoCreateView.as_view(), name='video-create'),
    path('video/<int:pk>/update/', views.VideoUpdateView.as_view(), name='video-update'),
    path('video/<int:pk>/delete/', views.VideoDeleteView.as_view(), name='video-delete'),
    path('user/<str:username>/', views.UserVideoListView.as_view(), name='user-videos'),
    path('video/<int:pk>/like/', views.like_video, name='like-video'),
    path('video/<int:pk>/dislike/', views.dislike_video, name='dislike-video'),
    path('video/<int:pk>/subscribe/', views.subscribe_to_channel, name='subscribe'),
    path('category/<int:pk>/', views.CategoryVideoListView.as_view(), name='category-videos'),
    path('search/', views.SearchResultsView.as_view(), name='search-results'),
    path('trending/', views.TrendingVideosView.as_view(), name='trending'),
    path('subscriptions/', views.SubscriptionsView.as_view(), name='subscriptions'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('liked/', views.LikedVideosView.as_view(), name='liked-videos'),
]
