"""
URL configuration for military_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from main import urls as main_app_urls
from accounts import urls as accounts_app_urls
from soldiers import urls as soldiers_app_urls
from units import urls as units_app_urls
from missions import urls as missions_app_urls
from notifications import urls as notifications_app_urls

handler403 = 'main.views.error_403'
handler404 = 'main.views.error_404'
handler500 = 'main.views.error_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(main_app_urls)),
    path('', include(accounts_app_urls)),
    path('', include(soldiers_app_urls)),
    path('', include(units_app_urls)),
    path('', include(missions_app_urls)),
    path('', include(notifications_app_urls)),
]

