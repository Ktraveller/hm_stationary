from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from stationary_system.models.accounts import Notification


# Admin site
@login_required(login_url='login_page_admin') 
def admin_notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).select_related('activity').order_by('-created_at')

    return render(request, 'admin/notifications.html', {
        "notifications": notifications
    })


@login_required(login_url='login_page_admin') 
def admin_user(request):
    user = request.user
    return render(request, "admin/user.html", {"user": user})


# Stationary site
@login_required(login_url='login_page_stationary') 
def notifications(request):
  return render(request, 'stationary/notifications.html')


@login_required(login_url='login_page_stationary') 
def user(request):
    user = request.user
    return render(request, "stationary/user.html", {"user": user})
