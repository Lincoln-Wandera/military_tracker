from django.shortcuts import render
from django.http import HttpRequest


def landing_page(request: HttpRequest):
      return render(request, 'pages/landingpage.html', {"name": "Military Soldiers Tracking and Notification System"})

def home_page(request: HttpRequest):
    return render(request, 'pages/home.html', {"name": "home"})

def error_403(request, exception):
    return render(request, 'pages/403.html', status=403)


def error_404(request, exception):
    return render(request, 'pages/404.html', status=404)


def error_500(request):
    return render(request, 'pages/500.html', status=500)
