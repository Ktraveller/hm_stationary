import os
from random import random
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from django.urls import reverse
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from mimetypes import guess_type


from stationary_system.models.accounts import Notification
from stationary_system.models.stationary import Area, StationaryProfile
from stationary_system.models.activity import Activity, DocumentFormat
from stationary_system.models.uploaded import UploadedFile


# printing
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.db import transaction


# printing documents
@login_required(login_url='login_page_customer')
def printing(request):
    if request.method == 'POST':
        try:
            status = "waiting"
            activity_type = "printing"
            stationary_id = request.POST.get('stationary_id')
            end_date = request.POST.get('end_date')
            files = request.FILES.getlist('files')

            font_family = request.POST.get('font_family')
            font_size = request.POST.get('font_size')
            text_alignment = request.POST.get('text_alignment')
            other_details = request.POST.get('other_details')

            if not stationary_id:
                return JsonResponse({"success": False, "error": "Stationary is required"})

            with transaction.atomic():

                while True:
                    last = Activity.objects.order_by('-id').first()
                    last_num = int(last.activity_id.split('-')[1]) if last and last.activity_id else 0
                    new_id = f"CA-{last_num + 1:04d}"

                    if not Activity.objects.filter(activity_id=new_id).exists():
                        break

                profile = StationaryProfile.objects.get(id=stationary_id)


                activity = Activity.objects.create(
                    activity_id=new_id,
                    stationary_profile=profile,
                    activity_type=activity_type,
                    costs = 0,
                    user=request.user,
                    status=status,
                    end_date=end_date if end_date else None
                )


                for f in files:
                    UploadedFile.objects.create(file=f, activity=activity)

                DocumentFormat.objects.create(
                    activity=activity,
                    font_family=font_family,
                    font_size=font_size,
                    text_alignment=text_alignment,
                    other_details=other_details
                )

                # send notification to stationary
                Notification.objects.create(
                    user=profile.user,  # stationary user
                    activity=activity,
                    message=f"New print request {activity.activity_id}"
                )

                return JsonResponse({
                    "success": True,
                    "next_url": redirect("preview_activity", activity_id=activity.activity_id).url
                })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            })

    stations = StationaryProfile.objects.prefetch_related('areas').all()
    return render(request, 'customer/printing.html', {'stations': stations})




# Typing and editing
@login_required(login_url='login_page_customer')
def typing_editing(request):
    if request.method == 'POST':
        try:
            status = "waiting"
            activity_type = "typing and editing"
            stationary_id = request.POST.get('stationary_id')
            end_date = request.POST.get('end_date')
            files = request.FILES.getlist('files')

            font_family = request.POST.get('font_family')
            font_size = request.POST.get('font_size')
            text_alignment = request.POST.get('text_alignment')
            other_details = request.POST.get('other_details')

            if not stationary_id:
                return JsonResponse({"success": False, "error": "Stationary is required"})

            with transaction.atomic():

                while True:
                    last = Activity.objects.order_by('-id').first()
                    last_num = int(last.activity_id.split('-')[1]) if last and last.activity_id else 0
                    new_id = f"CA-{last_num + 1:04d}"

                    if not Activity.objects.filter(activity_id=new_id).exists():
                        break

                profile = StationaryProfile.objects.get(id=stationary_id)


                activity = Activity.objects.create(
                    activity_id=new_id,
                    stationary_profile=profile,
                    activity_type=activity_type,
                    costs = 0,
                    user=request.user,
                    status=status,
                    end_date=end_date if end_date else None
                )


                for f in files:
                    UploadedFile.objects.create(file=f, activity=activity)

                DocumentFormat.objects.create(
                    activity=activity,
                    font_family=font_family,
                    font_size=font_size,
                    text_alignment=text_alignment,
                    other_details=other_details
                )

                # send notification to stationary
                Notification.objects.create(
                    user=profile.user,  # stationary user
                    activity=activity,
                    message=f"New print request {activity.activity_id}"
                )


                # send notification to customer
                Notification.objects.create(
                    user=request.user,  # user
                    activity=activity,
                    message=f"Your typing or editing request has been submitted successfully - {activity.activity_id}"
                )



                return JsonResponse({
                    "success": True,
                    "next_url": redirect("preview_activity", activity_id=activity.activity_id).url
                })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            })

    stations = StationaryProfile.objects.prefetch_related('areas').all()
    return render(request, 'customer/typing-editing.html', {'stations': stations})




# preview activity
@login_required(login_url='login_page_customer') 
def preview_activity(request, activity_id):
    activity = get_object_or_404(Activity, activity_id=activity_id, user=request.user)

    uploaded_files_qs = UploadedFile.objects.filter(
        activity=activity, file__isnull=False
    ).exclude(file='')

    processed_files_qs = UploadedFile.objects.filter(
        activity=activity, processed_file__isnull=False
    ).exclude(processed_file='')

    uploaded_files = []
    for f in uploaded_files_qs:
        try:
            if f.file and os.path.exists(f.file.path):
                mime, _ = guess_type(f.file.name)

                uploaded_files.append({
                    'file': f,
                    'is_image': mime and mime.startswith('image'),
                    'size': f.file.size,
                })
        except (FileNotFoundError, ValueError):
            continue  # skip broken file safely

    processed_files = []
    for f in processed_files_qs:
        try:
            if f.processed_file and os.path.exists(f.processed_file.path):
                mime, _ = guess_type(f.processed_file.name)

                processed_files.append({
                    'file': f,
                    'is_image': mime and mime.startswith('image'),
                    'size': f.processed_file.size,
                })
        except (FileNotFoundError, ValueError):
            continue  # skip broken file safely

    # Stationary name
    activity.stationary_name = (
        activity.stationary_profile.stationary_name
        if activity.stationary_profile else "N/A"
    )

    context = {
        'activity': activity,
        'uploaded_files': uploaded_files,
        'processed_files': processed_files,
    }
    return render(request, 'customer/preview-activity.html', context)



# delete pending activity
@login_required(login_url='login_page_customer')
def delete_pending_activity(request, activity_id):
    if request.method == "POST":
        try:
            activity = get_object_or_404(
                Activity,
                activity_id=activity_id,
                user=request.user,
                status__in=['pending', 'waiting', 'completed']
            )

            uploaded_files = UploadedFile.objects.filter(activity=activity)

            for f in uploaded_files:
                if f.file:
                    f.file.delete()
                if hasattr(f, 'processed_file') and f.processed_file:
                    f.processed_file.delete()
                f.delete()

            activity.delete()

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})




# Edit activity
@login_required(login_url='login_page_customer')
def edit_activity(request, activity_id):

    activity = get_object_or_404(
        Activity.objects.select_related('document_format'),
        activity_id=activity_id,
        user=request.user
    )

    document_format = getattr(activity, 'document_format', None)

    if request.method == "POST":
        try:
            with transaction.atomic():

                # =========================
                # 1. Update Stationary
                # =========================
                stationary_id = request.POST.get('stationary_id')

                if stationary_id:
                    activity.stationary_profile = get_object_or_404(
                        StationaryProfile,
                        id=stationary_id
                    )
                    activity.save()

                # =========================
                # 2. Document Format (OneToOne)
                # =========================
                font_family = request.POST.get('font_family')
                font_size = request.POST.get('font_size')
                text_alignment = request.POST.get('text_alignment')
                other_details = request.POST.get('other_details')

                document_format, created = DocumentFormat.objects.get_or_create(
                    activity=activity
                )

                if font_family:
                    document_format.font_family = font_family

                if font_size:
                    document_format.font_size = font_size

                if text_alignment:
                    document_format.text_alignment = text_alignment

                if other_details:
                    document_format.other_details = other_details

                document_format.save()

                # =========================
                # 3. Uploaded Files
                # =========================
                new_files = request.FILES.getlist('files')

                UploadedFile.objects.bulk_create([
                    UploadedFile(
                        activity=activity,
                        file=f,
                        processed_file=None
                    )
                    for f in new_files
                ])

            return JsonResponse({
                "success": True,
                "message": "Activity updated successfully!",
                "next_url": reverse("preview_activity", args=[activity_id])
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": f"Failed to update activity: {str(e)}"
            })

    # =========================
    # GET REQUEST
    # =========================
    uploaded_files_qs = activity.uploaded_files.all()
    safe_uploaded_files = []

    for f in uploaded_files_qs:
        try:
            if f.file and hasattr(f.file, 'path') and os.path.exists(f.file.path):
                safe_uploaded_files.append(f)
        except (FileNotFoundError, ValueError):
            continue  # skip broken file

    stations = StationaryProfile.objects.prefetch_related('areas').all()

    return render(request, 'customer/edit-activity.html', {
        "activity": activity,
        "uploaded_files": safe_uploaded_files,
        "stations": stations,
        "document_format": document_format
    })


# Delete individual file
@login_required(login_url='login_page_customer')
def delete_uploaded_file(request, file_id):
    if request.method == "POST":
        uploaded_file = get_object_or_404(UploadedFile, id=file_id, activity__user=request.user)
        if uploaded_file.file:
            uploaded_file.file.delete()
        uploaded_file.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Invalid request"})



# aActivity history
@login_required(login_url='login_page_customer')
def customer_activity_history(request):
    activities = Activity.objects.filter(user=request.user)\
        .prefetch_related('uploaded_files')\
        .order_by('-sent_date')

    return render(request, 'customer/activities-history.html', {
        'activities': activities
    })



# download processed file
@login_required(login_url='login_page_customer')
def download_processed_file(request, file_id):
    try:
        obj = UploadedFile.objects.get(id=file_id, activity__user=request.user)
        file_path = obj.processed_file.path
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    except UploadedFile.DoesNotExist:
        raise Http404("File not found")