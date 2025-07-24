from django.urls import path
from .views import unit_list, unit_detail, unit_create, unit_update, unit_home

urlpatterns = [
    path('units/', unit_list, name='unit_list'),
    path('<int:pk>/unit-detail/', unit_detail, name='unit_detail'),
    path('create-unit/', unit_create, name='unit_create'),
    path('<int:pk>/edit-unit/', unit_update, name='unit_update'),
    path('units-home/', unit_home, name='unit_home'),
]
