from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count
from stationary_system.models.accounts import Notification
from stationary_system.models.stationary import StationaryProfile
from stationary_system.models.activity import Activity

User = get_user_model()


@login_required(login_url='login_page_customer') 
def customer_dashboard(request):
    # Get all user activities
    activities = Activity.objects.filter(user=request.user).order_by('-sent_date')[:10]  # Get the latest 10 activities

    return render(request, 'customer/dashboard.html', {
        'activities': activities
    })




# more services
@login_required(login_url='login_page_customer') 
def more_services(request):
    return render(request, 'customer/more-services.html')


# payment page
@login_required(login_url='login_page_customer') 
def make_payment(request, activity):
    activity = get_object_or_404(Activity, activity_id=activity, user=request.user)
    return render(request, 'customer/payment.html', {'activity': activity})



# implementation pages
@login_required(login_url='login_page_customer') 
def implementation(request):
    return render(request, 'customer/implementation.html')

# profile customer
@login_required(login_url='login_page_customer') 
def profile(request):
    return render(request, 'customer/profile.html')
    

# help
@login_required(login_url='login_page_customer') 
def help(request):
    return render(request, 'customer/help.html')

# demo pages
def demo(request):
    return render(request, 'customer/demo/dashboard.html')
