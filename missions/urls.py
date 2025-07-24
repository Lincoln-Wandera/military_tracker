from django.urls import path
from .views import mission_list, mission_detail, mission_create, mission_update, assign_soldier, mission_home

urlpatterns = [
    path('mission-list/', mission_list, name='mission_list'),
    path('<int:pk>-mission-detail/', mission_detail, name='mission_detail'),
    path('mission-create/', mission_create, name='mission_create'),
    path('<int:pk>-mission-edit/', mission_update, name='mission_update'),
    path('assign-soldier/', assign_soldier, name='assign_soldier'),
    path('missions-home/', mission_home, name='mission_home'),
]

