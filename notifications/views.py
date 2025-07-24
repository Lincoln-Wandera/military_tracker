from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification
from .forms import NotificationForm
from django.utils.timezone import now

@login_required
def notification_list(request):
    if request.user.role == 'family':
        notifications = Notification.objects.filter(family=request.user)
    else:
        notifications = Notification.objects.all()
    return render(request, 'notification/list.html', {'notifications': notifications})

@login_required
def notification_detail(request, pk):
    notif = get_object_or_404(Notification, pk=pk)

    if notif.family != request.user and request.user.role == 'family':
        return redirect('notification_list')  # deny access to others

    if not notif.is_read:
        notif.is_read = True
        notif.read_at = now()
        notif.save()

    return render(request, 'notification/detail.html', {'notif': notif})

@login_required
def notification_create(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notif = form.save(commit=False)
            notif.is_sent = True
            notif.sent_at = now()
            notif.save()
            return redirect('notification_list')
    else:
        form = NotificationForm()
    return render(request, 'notification/create.html', {'form': form})

@login_required
def notification_home(request):
    if request.user.role != 'admin':
        raise PermissionDenied
    return render(request, 'notification/notification.html', {}) 