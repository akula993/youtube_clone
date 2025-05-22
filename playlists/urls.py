from django.urls import path
from . import views

urlpatterns = [

    path('', views.PlaylistListView.as_view(), name='playlist-list'),
    path('<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist-detail'),
    path('create/', views.PlaylistCreateView.as_view(), name='playlist-create'),
    path('<int:pk>/update/', views.PlaylistUpdateView.as_view(), name='playlist-update'),
    path('<int:pk>/delete/', views.PlaylistDeleteView.as_view(), name='playlist-delete'),
    path('add-to-playlist/', views.add_to_playlist, name='add-to-playlist'),
    path('<int:playlist_id>/remove/<int:video_id>/', views.remove_from_playlist, name='remove-from-playlist'),
    path('<int:playlist_id>/reorder/', views.reorder_playlist, name='reorder-playlist'),
    path('get-playlists/<int:video_id>/', views.get_user_playlists, name='get-user-playlists'),
]
