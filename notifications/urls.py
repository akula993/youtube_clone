from django.urls import path
from . import views

urlpatterns = [

    path('', views.NotificationListView.as_view(), name='notifications'),
    path('mark-read/<int:pk>/', views.mark_notification_read, name='mark-notification-read'),
    path('mark-all-read/', views.mark_all_notifications_read, name='mark-all-read'),
    path('preferences/', views.NotificationPreferencesView.as_view(), name='notification-preferences'),
]
