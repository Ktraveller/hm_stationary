from urllib import request

from django.contrib.auth.models import User, Group

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from stationary_system.models.stationary import StationaryProfile, Area
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404
from django.shortcuts import get_object_or_404, redirect

import random, string, re
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required(login_url='login_page_admin') 
def admin_stationaries(request):
  # Get all stationary profiles with related user
    stationary_profiles = StationaryProfile.objects.select_related('user').all()
    return render(request, 'admin/stationaries.html', {
        'stationary_profiles': stationary_profiles
    })


# register stationary form
@login_required(login_url='login_page_admin') 
def register_stationary(request):
  return render(request, 'admin/register_stationary.html')


# register validation
@login_required(login_url='login_page_admin') 
def register_validation(request):
    stationary_name_p = request.POST.get('stationary_name', '').strip()
    phone_p = request.POST.get('phone', '').strip()
    email_p = request.POST.get('email', '').strip()
    payment_number_p = request.POST.get('payment_number', '').strip()
    payment_name_p = request.POST.get('payment_name', '').strip()

    # Validate name (letters and spaces only)
    if not re.match(r'^[A-Za-z\s]+$', stationary_name_p):
        messages.error(request, "Name should not contain special characters.")
        return HttpResponseRedirect(reverse('register_stationary'))

    # Validate phone (numeric and <=11 digits)
    if not phone_p.isdigit() or len(phone_p) > 11:
        messages.error(request, "Phone must be numeric and at most 11 digits.")
        return HttpResponseRedirect(reverse('register_stationary'))

    # Check if phone already exists in StationaryProfile
    if StationaryProfile.objects.filter(phone=phone_p).exists():
        messages.error(request, "Phone number already exists.")
        return HttpResponseRedirect(reverse('register_stationary'))

    # Check if email already exists in User
    if email_p and User.objects.filter(email=email_p).exists():
        messages.error(request, "Email already exists.")
        return HttpResponseRedirect(reverse('register_stationary'))

    # Generate UNIQUE stationary ID
    for _ in range(10):
        generate_id = ''.join(random.choices(string.digits, k=6))
        stationary_identity = f"S-{generate_id}"
        if not User.objects.filter(username=stationary_identity).exists():
            break
    else:
        messages.error(request, "Could not generate unique stationary ID. Try again.")
        return HttpResponseRedirect(reverse('register_stationary'))

    # Default password = stationary_id
    default_password = stationary_identity

    # add data in session
    request.session['stationary_name'] = stationary_name_p
    request.session['phone'] = phone_p
    request.session['email'] = email_p
    request.session['stationary_id'] = stationary_identity
    request.session['default_password'] = default_password
    request.session['payment_number'] = payment_number_p
    request.session['payment_name'] = payment_name_p

    return HttpResponseRedirect(reverse('save_stationary'))

# save stationary data
@login_required(login_url='login_page_admin')
def save_stationary(request):
    if request.method == "POST":
        # Get session data
        stationary_name = request.session.get('stationary_name')
        phone = request.session.get('phone')
        email = request.session.get('email')
        stationary_id = request.session.get('stationary_id')
        default_password = request.session.get('default_password')
        payment_number_p = request.session.get('payment_number')
        payment_name_p = request.session.get('payment_name')

        # Get location from POST (sent via JS)
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Validate required data
        if not all([stationary_name, phone, stationary_id, default_password]):
            messages.error(request, "Missing data. Please register again.")
            return HttpResponseRedirect(reverse('register_stationary'))

        # Check if user already exists
        if User.objects.filter(username=stationary_id).exists():
            messages.error(request, f"User with ID '{stationary_id}' already exists.")
            return HttpResponseRedirect(reverse('register_stationary'))

        # Create Django User
        user = User.objects.create(
            username=stationary_id,
            password=make_password(default_password),
            email=email,
            first_name=stationary_name
        )

        # Add user to 'stationary' group
        try:
            group = Group.objects.get(name='stationary')
            user.groups.add(group)
        except Group.DoesNotExist:
            messages.warning(request, "Group 'stationary' not found. User added without group.")

        # Create StationaryProfile
        stationary = StationaryProfile.objects.create(
            user=user,
            stationary_name=stationary_name,
            phone=phone,
            force_password_change=True,
            payment_no=payment_number_p,
            payment_name=payment_name_p,
        )

        # Save Area if location provided
        if latitude and longitude:
            try:
                Area.objects.create(
                    stationary=stationary,  # ✅ must pass StationaryProfile instance
                    latitude=float(latitude),
                    longitude=float(longitude)
                )
            except ValueError:
                messages.warning(request, "Invalid coordinates. Area not saved.")

        # Clear session data
        for key in ['stationary_name', 'phone', 'email', 'stationary_id', 'default_password']:
            request.session.pop(key, None)

        messages.success(request, f"Stationary '{stationary_name}' registered successfully with ID {stationary_id}.")
        return HttpResponseRedirect(reverse('save_stationary'))

    return render(request, 'admin/save_stationary.html')




# stationary preview
@login_required(login_url='login_page_admin') 
def preview_stationary(request, username):
    # Get the user and related profile
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(StationaryProfile, user=user)

    return render(request, "admin/stationary.html", {
        "user": user,
        "profile": profile
    })


# delete stationary
@login_required(login_url='login_page_admin')
def delete_stationary(request, username):
    profile = get_object_or_404(StationaryProfile, user__username=username)

    if request.method == "POST":
        profile.user.delete()  # deletes user + cascades profile

        return redirect('admin_stationaries')