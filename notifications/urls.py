from django.urls import path
from .views import notification_create, notification_list, notification_detail, notification_home

urlpatterns = [
    path('notification-list/', notification_list, name='notification_list'),
    path('<int:pk>-notification-detail/', notification_detail, name='notification_detail'),
    path('create-notification/', notification_create, name='notification_create'),
    path('notification-home/', notification_home, name='notification_home'),
]
