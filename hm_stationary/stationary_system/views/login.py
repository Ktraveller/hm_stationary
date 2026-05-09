import re
import string
import random

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.db import transaction


from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse

from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()
from django.views.decorators.csrf import csrf_exempt


CustomUser = get_user_model()

# login for admin
def login_page_admin(request):
    if request.method == 'POST':
        identifier = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        user = None

        # Admin: first superuser
        admin_user = CustomUser.objects.filter(is_superuser=True).first()
        if admin_user and admin_user.username == identifier:
            user = authenticate(request, username=admin_user.username, password=password)

        if user:
            login(request, user)

            # redirect based on type
            if user.is_superuser:
                return redirect("admin_dashboard")
            
        else:
            messages.error(request, "Invalid credentials!")

    return render(request, "admin/login_admin.html")



# login for stationary
def login_page_stationary(request):
    if request.method == "POST":
        stationary_id = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=stationary_id, password=password)

        if user:
            if user.groups.filter(name='stationary').exists():
                login(request, user)
                return JsonResponse({
                    "status": "success",
                    "message": "Login successful! Welcome.",
                    "redirect_url": reverse('stationary_dashboard')  # use path name here
                })
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "You do not have permission to login as stationary."
                })
        else:
            return JsonResponse({
                "status": "error",
                "message": "Invalid stationary ID or password."
            })

    # For GET requests, just render the template normally
    return render(request, "stationary/login_stationary.html")




# auto signup for customer
@transaction.atomic
def signup(request):

    # ✅ Lock latest customer row to prevent duplicate IDs
    last_user = (
        CustomUser.objects
        .select_for_update()
        .filter(username__startswith="CU")
        .order_by("-username")
        .first()
    )

    # ✅ Generate next ID safely
    if last_user:
        last_number = int(last_user.username.replace("CU", ""))
        new_number = last_number + 1
    else:
        new_number = 0

    user_id = f"CU{new_number:04d}"

    # ✅ Generate secure random password
    password = ''.join(
        random.choices(string.ascii_letters + string.digits, k=8)
    )

    # ✅ Create user
    user = CustomUser.objects.create_user(
        username=user_id,
        password=password
    )

    # ✅ Add user to customer group
    group, created = Group.objects.get_or_create(name='customer')
    user.groups.add(group)

    # ✅ Auto login
    login(request, user)

    # redirect to customer dashboard
    return redirect('customer_dashboard')

# return home
def login_customer(request):
    return render(request, "customer/login_customer.html")


# change password
@login_required
@csrf_exempt
def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password", "").strip()
        new_password = request.POST.get("new_password", "").strip()

        user = request.user

        # Check old password
        if not user.check_password(old_password):
            return JsonResponse({
                "status": "error",
                "message": "Current password is incorrect"
            })

        # Validate new password (basic)
        if len(new_password) < 4:
            return JsonResponse({
                "status": "error",
                "message": "Password must be at least 4 characters"
            })

        # Set new password
        user.set_password(new_password)
        user.save()

        # Keep user logged in after password change
        update_session_auth_hash(request, user)

        return JsonResponse({
            "status": "success",
            "message": "Password changed successfully!"
        })

    return JsonResponse({
        "status": "error",
        "message": "Invalid request"
    })



# logout
def stationary_logout(request):
    logout(request)
    return redirect('login_page_stationary')

def admin_logout(request):
    logout(request)
    return redirect('login_page_admin')

def customer_logout(request):
    logout(request)
    return redirect('login_page_customer')




def ping(request):
    return HttpResponse("OK")