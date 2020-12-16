from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from notifications.models import Notification
from django.db import transaction

# Create your views here.


@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('datetime')
    with transaction.atomic():
        for notification in notifications.filter(is_viewed=False):
            notification.is_viewed = True
            notification.save()
    context = {
        'notifications': notifications,
    }
    return render(request, 'notifications/notifications.html', context)
