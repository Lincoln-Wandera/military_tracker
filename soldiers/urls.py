from django.urls import path
from .views import admin_link_family, soldier_list, soldier_detail, soldier_create, soldier_update, family_dashboard, soldier_home, soldier_status_history, link_to_soldier, unlink_soldier, admin_link_family, add_emergency_contact, delete_emergency_contact, edit_emergency_contact, family_emergency_contacts

urlpatterns = [
    path('soldier-list/', soldier_list, name='soldier_list'),
    path('<int:pk>-soldier-detail/', soldier_detail, name='soldier_detail'),
    path('create-soldier/', soldier_create, name='soldier_create'),
    path('<int:pk>-soldier-edit/', soldier_update, name='soldier_update'),
    path('family-dashboard/', family_dashboard, name='family_dashboard'),
    path('soldiers-home/', soldier_home, name='soldier_home'),
    path('<int:pk>/status-history/', soldier_status_history, name='soldier_status_history'),
    path('link-soldier/', link_to_soldier, name='link_to_soldier'),
    path('unlink/<int:pk>/', unlink_soldier, name='unlink_soldier'),
    path('admin-link-family/', admin_link_family, name='admin_link_family'),
    path('<int:soldier_id>/contacts/add/', add_emergency_contact, name='add_emergency_contact'),
    path('contacts/<int:contact_id>/delete/', delete_emergency_contact, name='delete_emergency_contact'),
    path('family/emergency-contacts/', family_emergency_contacts, name='family_emergency_contacts'),
    path('contacts/<int:contact_id>/edit/', edit_emergency_contact, name='edit_emergency_contact'),


]