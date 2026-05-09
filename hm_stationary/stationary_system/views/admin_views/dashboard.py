from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum
from decimal import Decimal
from django.contrib.auth.models import Group
from stationary_system.models.accounts import CustomUser
from stationary_system.models.activity import Activity
from stationary_system.models.payments import Payments
from stationary_system.models.stationary import StationaryProfile


@login_required(login_url='login_page_admin') 
def admin_dashboard(request):

    # Total activities (ALL statuses)
    total_activities = Activity.objects.count()

    # Total stationary users
    total_stationary = StationaryProfile.objects.count()

    # Total customer
    total_customer = Group.objects.get(name='customer').user_set.count()

    # Total payments made
    total_payments = Payments.objects.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')

    # Total activity costs (ALL activities, regardless of status)
    total_costs = Activity.objects.aggregate(
        total=Sum('costs')
    )['total'] or Decimal('0.00')

    # Admin income = 10% of total income from payments
    income = Decimal('0.00')
    if total_payments > Decimal('0.00'):
        income = total_payments * Decimal('0.10')

    return render(request, 'admin/dashboard.html', {
        "total_activities": total_activities,
        "total_stationary": total_stationary,
        "total_customers": total_customer,
        
        "total_payments": total_payments,
        "total_costs": total_costs,
        "income": income
    })