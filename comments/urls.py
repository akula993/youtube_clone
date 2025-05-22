
from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:video_id>/', views.create_comment, name='create-comment'),
    path('reply/<int:comment_id>/', views.reply_comment, name='reply-comment'),
    path('like/<int:comment_id>/', views.like_comment, name='like-comment'),
    path('dislike/<int:comment_id>/', views.dislike_comment, name='dislike-comment'),
    path('delete/<int:comment_id>/', views.delete_comment, name='delete-comment'),
]

