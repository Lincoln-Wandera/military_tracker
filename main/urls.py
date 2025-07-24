from django.urls import path
from .views import landing_page, home_page

urlpatterns = [
    path('', landing_page, name='home'),
    path('home/', home_page, name='home_page'),
]
