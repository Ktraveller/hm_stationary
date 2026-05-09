from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from stationary_system.models.accounts import Notification



# get notifications
@login_required(login_url='login_page_stationary')
def get_notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:20]

    data = []
    unread_count = 0

    for n in notifications:
        if not n.is_read:
            unread_count += 1

        data.append({
            "id": n.id,
            "message": n.message,
            "is_read": n.is_read,

            # ✅ FIX: safe access (avoid crash if activity is None)
            "activity_id": getattr(n.activity, "activity_id", None)
        })

    return JsonResponse({
        "notifications": data,
        "unread_count": unread_count
    })



@login_required(login_url='login_page_stationary')
@csrf_exempt
@require_POST
def mark_notification_read(request):

    notif_id = request.POST.get("id")

    try:
        notif = Notification.objects.get(
            id=notif_id,
            user=request.user
        )

        notif.is_read = True
        notif.save()

        return JsonResponse({"success": True})

    except Notification.DoesNotExist:
        return JsonResponse({"success": False})



@login_required(login_url='login_page_stationary')
@csrf_exempt
@require_POST
def delete_notification(request):

    notif_id = request.POST.get("id")

    try:
        notif = Notification.objects.get(
            id=notif_id,
            user=request.user
        )

        notif.delete()

        return JsonResponse({"success": True})

    except Notification.DoesNotExist:
        return JsonResponse({"success": False}, status=404)