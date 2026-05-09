import json
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from stationary_system.models.stationary import StationaryProfile
from stationary_system.models.activity import Activity
from stationary_system.models.accounts import Notification
from stationary_system.models.payments import Payments
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()



@login_required(login_url='login_page_customer')
def submit_payment(request):
    if request.method == "POST":

        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"success": False, "error": "Invalid JSON"})

            amount = data.get("amount_paid")
            phone = data.get("phone_number")
            activity = data.get("activity")
            stationary_id = data.get("stationary_id")

        else:
            # fallback for normal form POST
            amount = request.POST.get("amount_paid")
            phone = request.POST.get("phone_number")
            activity = request.POST.get("activity")
            stationary_id = request.POST.get("stationary_id")

        activity_p = Activity.objects.get(activity_id=activity)
        description = f"Activity payments - {activity_p}"

        # Validation
        # ---------------------------
        # ---------------------------
        # Amount Validation
        # ---------------------------
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except (TypeError, ValueError):
            return JsonResponse({"success": False, "error": "Invalid amount"})


        # ---------------------------
        # Phone Validation
        # ---------------------------
        phone = str(phone).strip()

        # Remove leading 0 (same as frontend)
        if phone.startswith("0"):
            phone = phone[1:]

        # Check digits only + exactly 9 digits
        if not phone.isdigit() or len(phone) != 9:
            return JsonResponse({
                "success": False,
                "error": "Phone number must be exactly 9 digits"
            })
        
        stationary = StationaryProfile.objects.get(id=stationary_id)

        payment = Payments.objects.create(
            user=request.user,
            stationary_profile=stationary,
            amount=amount,
            phone_used=phone,
            description=description,
            paid_at = timezone.now() 
        )


    admins = User.objects.filter(is_superuser=True)
    activity = Activity.objects.get(activity_id=activity)
    activity.status = "pending"
    activity.save()

    for admin in admins:
        Notification.objects.create(
            user=admin,
            activity=activity,
            message=f"New payment submitted by customer, ID - {activity}"
        )

    # Notify stationary
    if activity.stationary_profile:
        Notification.objects.create(
            user=activity.stationary_profile.user,
            activity=activity,
            message=f"New payment submitted for your stationary, Activity ID - {activity}"
        )


        return JsonResponse({
            "success": True,
            "message": "Payment recorded successfully",
            "payment_id": payment.id
        })

    return JsonResponse({"success": False, "error": "Invalid request method"})
