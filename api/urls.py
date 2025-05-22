from django.urls import path
from . import views

urlpatterns = [
    path('clear-history/', views.clear_history_api, name='api-clear-history'),
    path('search-videos/', views.search_videos_api, name='api-search-videos'),
]
