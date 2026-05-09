from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from stationary_system.models.accounts import Notification
from stationary_system.models.activity import Activity
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST

# Activity list
@login_required(login_url='login_page_admin') 
def admin_activities(request):
    activities = Activity.objects.all().order_by('-sent_date')  # Latest first
    context = {
        'activities': activities
    }
    return render(request, 'admin/activities.html', context)


# Activity preview
@login_required(login_url='login_page_admin')
def preview_activity(request, activity_id):
    activity = get_object_or_404(Activity, activity_id=activity_id)
    context = {
        'activity': activity
    }
    return render(request, 'admin/activity.html', context)


# Delete activity
@login_required(login_url='login_page_admin')
def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, activity_id=activity_id)

    if request.method == "POST":
        # Delete all related uploaded files
        uploaded_files = activity.uploaded_files.all()

        for uploaded in uploaded_files:
            # Delete actual files from media
            if uploaded.file:
                uploaded.file.delete(save=False)

            if uploaded.processed_file:
                uploaded.processed_file.delete(save=False)

            # Delete file record
            uploaded.delete()

        #  Delete activity
        activity.delete()

        return redirect('admin_activities')
    

# edit activity status
@login_required(login_url='login_page_admin')
def mark_activity_pending(request):
    if request.method == "POST":
        activity_id = request.POST.get('activity_id')
        activity = Activity.objects.get(activity_id=activity_id)
        activity.status = "pending"
        activity.save()

        return redirect('admin_notifications')
    

# delete activity notification
@login_required(login_url='login_page_admin')
def delete_notifications(request):
    if request.method == "POST":
        notification_id = request.POST.get('notification_id')
        notification = Notification.objects.get(id=notification_id)
        notification.delete()

        return redirect('admin_notifications')