from django.urls import path
from .views import delete_account, register_view, login_view, logout_view, profile_view, delete_account, edit_profile_view, change_password
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path('delete-account/', delete_account, name='delete_account'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('change-password/', change_password, name='change_password'),
]


