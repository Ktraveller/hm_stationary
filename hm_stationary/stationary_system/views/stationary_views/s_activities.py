from urllib import request

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from stationary_system.models.accounts import Notification
from stationary_system.models.activity import Activity, DocumentFormat
from stationary_system.models.uploaded import UploadedFile
from django.urls import reverse  # Add this import
from django.contrib import messages
from django.utils import timezone
import zipfile
from io import BytesIO

import os
from django.shortcuts import get_object_or_404, render


@login_required(login_url='login_page_stationary') 
def stationary_activities(request):
    query = request.GET.get('q', '')
    limit = request.GET.get('limit', 10)

    try:
        limit = int(limit)
    except ValueError:
        limit = 10

    # Get stationary profile for logged-in user
    try:
        profile = request.user.stationaryprofile
    except AttributeError:
        profile = None

    # Filter activities for this stationary
    if profile:
        activities = Activity.objects.filter(
            stationary_profile=profile
        ).order_by('-id')
    else:
        activities = Activity.objects.none()

    # Apply search filter
    if query:
        activities = activities.filter(
            Q(activity_id__icontains=query) |
            Q(user__username__icontains=query)
        )

    # Limit results
    activities = activities[:limit]

    # AJAX response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = []
        for i, act in enumerate(activities, 1):
            data.append({
                "index": i,
                "id": act.activity_id,
                "type": act.activity_type,
                "customer": act.user.username if act.user else "",
                "date": act.sent_date.strftime("%Y-%m-%d") if act.sent_date else "",
                "end_date": act.end_date.strftime("%Y-%m-%d") if act.end_date else "",
                "status": act.status,
                "url": reverse("preview_stationary_activity", args=[act.activity_id]) if act.activity_id else None
            })
        return JsonResponse(data, safe=False)

    return render(request, "stationary/activities.html", {
        "activities": activities,
        "stationary_name": profile.stationary_name if profile else "",
        "profile": profile
    })


# preview activity details
@login_required(login_url='login_page_stationary') 
def preview_stationary_activity(request, activity_id):
    activity = get_object_or_404(Activity, activity_id=activity_id)

    uploaded_files_qs = UploadedFile.objects.filter(
        activity=activity,
        file__isnull=False
    ).exclude(file='')

    processed_files_qs = UploadedFile.objects.filter(
        activity=activity,
        processed_file__isnull=False
    ).exclude(processed_file='')

    safe_uploaded_files = []
    for f in uploaded_files_qs:
        try:
            if f.file and hasattr(f.file, 'path') and os.path.exists(f.file.path):
                safe_uploaded_files.append(f)
        except (FileNotFoundError, ValueError):
            continue

    safe_processed_files = []
    for f in processed_files_qs:
        try:
            if f.processed_file and hasattr(f.processed_file, 'path') and os.path.exists(f.processed_file.path):
                safe_processed_files.append(f)
        except (FileNotFoundError, ValueError):
            continue

    context = {
        "activity": activity,
        "uploaded_files": safe_uploaded_files,
        "processed_files": safe_processed_files
    }

    return render(request, "stationary/activity.html", context)




# process activity
@login_required(login_url='login_page_stationary')
def process_activity(request, activity_id):
    activity = get_object_or_404(Activity, activity_id=activity_id)

    if request.method != "POST":
        return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

    files = request.FILES.getlist("processed_file")

    if not files:
        return JsonResponse({'success': False, 'message': 'No files uploaded.'}, status=400)

    # ----------------------------
    # Validation: Maximum 5 files
    # ----------------------------
    if len(files) > 5:
        return JsonResponse({'success': False, 'message': 'You can upload a maximum of 5 files at a time.'}, status=400)

    # ----------------------------
    # Validation: Allowed file types and max size
    # ----------------------------
    allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.doc', '.docx']
    max_file_size = 5 * 1024 * 1024  # 5MB in bytes

    for file in files:
        name = file.name.lower()
        # Check extension
        if not any(name.endswith(ext) for ext in allowed_extensions):
            return JsonResponse({'success': False,
                                 'message': f'File "{file.name}" is not allowed. Allowed types: PDF, PNG, JPG, JPEG, DOC, DOCX.'},
                                status=400)
        # Check size
        if file.size > max_file_size:
            return JsonResponse({'success': False,
                                 'message': f'File "{file.name}" exceeds the 5MB size limit.'},
                                status=400)

    # ----------------------------
    # Save each processed file
    # ----------------------------
    for file in files:
        UploadedFile.objects.create(
            activity=activity,
            processed_file=file
        )

    # ----------------------------
    # Update activity status
    # ----------------------------
    activity.status = 'completed'
    activity.end_date = timezone.now()
    activity.save()

    # Save notification ONLY (no real-time push)
    Notification.objects.create(
        user=activity.user,
        activity=activity,
        message=f"Activity processing completed, visit {request.user.stationaryprofile.stationary_name} to get your document or can you download it in system"
    )

    return JsonResponse({'success': True, 'message': 'Activity processed successfully!'})




# download all activity files
@login_required(login_url='login_page_stationary')
def download_all_files(request, activity_id):
    activity = get_object_or_404(Activity, activity_id=activity_id)

    files = activity.uploaded_files.filter(file__isnull=False).exclude(file='')
    

    if not files.exists():
        return HttpResponse("No files to download", status=404)

    # 🔹 Get DocumentFormat (if exists)
    doc_format = DocumentFormat.objects.filter(activity=activity).first()

    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:

        # 🔹 1. Add uploaded files
        for f in files:
            if f.file and f.file.name:
                zip_file.write(f.file.path, f.file.name)

        # 🔹 2. Build text content
        activity_text = f"""
========== ACTIVITY DETAILS ==========
Activity ID: {activity.activity_id}
Activity Type: {activity.activity_type}

User: {activity.user}
Status: {activity.status}

Sent Date: {activity.sent_date}
End Date: {activity.end_date}

"""

        # 🔹 3. Append DocumentFormat if available
        if doc_format:
            activity_text += f"""


========== DOCUMENT FORMAT ==========
Font Family: {doc_format.font_family}
Font Size: {doc_format.font_size}
Text Alignment: {doc_format.text_alignment}
other_details: {doc_format.other_details}
"""
        else:
            activity_text += "\n\nNo Document Format found."

        # 🔹 4. Add text file into ZIP
        zip_file.writestr("activity_details.txt", activity_text)

    zip_buffer.seek(0)

    response = HttpResponse(zip_buffer.read(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="activity_{activity_id}_files.zip"'

    return response





# send cost to customer
@login_required(login_url='login_page_stationary')
def send_cost(request):

    if request.method == 'POST':

        activity_id = request.POST.get('activity_id')
        costs = request.POST.get('costs')

        if not activity_id or not costs:
            return JsonResponse(
                {'success': False, 'message': 'Missing data'},
                status=400
            )

        activity = get_object_or_404(Activity, activity_id=activity_id)

        # Save cost
        activity.costs = costs
        activity.save()

        # Save notification ONLY (no real-time push)
        notification = Notification.objects.create(
            user=activity.user,
            activity=activity,
            message=f"Your activity cost has been set to Tsh {costs}"
        )

        return JsonResponse({
            'success': True,
            'message': 'Cost updated successfully',
            'notif': {
                'id': notification.id,
                'message': notification.message,
                'activity_id': activity.activity_id
            }
        })

    return JsonResponse(
        {'success': False, 'message': 'Invalid request'},
        status=400
    )



# accept activity
@login_required(login_url='login_page_stationary')
def accept_activity(request, activity_id):
    if request.method == 'POST':
        activity = get_object_or_404(Activity, activity_id=activity_id)
        activity.status = 'processing'
        activity.save()

        # Save notification ONLY (no real-time push)
        Notification.objects.create(
            user=activity.user,
            activity=activity,
            message=f"Activity accepted and now processing."
        )
        return JsonResponse({'success': True, 'message': 'Activity accepted and now processing.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)



# decline activity
@login_required(login_url='login_page_stationary')
def decline_activity(request, activity_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

    activity = get_object_or_404(Activity, activity_id=activity_id)

    if activity.status != 'declined':
        activity.status = 'declined'
        activity.save()

        # Save notification ONLY (no real-time push)
        Notification.objects.create(
            user=activity.user,
            activity=activity,
            message=f"Activity declined by stationary."
        )        
        return JsonResponse({'success': True, 'message': 'Activity declined successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'Activity already declined.'})
    


