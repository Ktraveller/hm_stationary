from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from decimal import Decimal
from stationary_system.models import stationary
from stationary_system.models.activity import Activity


# stationary dashboard
@login_required(login_url='login_page_stationary')
def stationary_dashboard(request):

    stationary = request.user.stationaryprofile

    total_costs = Activity.objects.filter(
        stationary_profile=stationary,
        status='completed'
    ).aggregate(total_cost=Sum('costs'))['total_cost'] or Decimal('0.00')

    # get bonus
    bonus = Decimal('0.00')
    if total_costs > Decimal():
        bonus = total_costs * Decimal('0.10')  # 10%

    # stationary earn
    total_earn = total_costs - bonus

    # total activity
    total_activities = Activity.objects.filter(
        stationary_profile=stationary,
        status='completed'
    ).count()

    # total printing
    total_printing = Activity.objects.filter(
        stationary_profile=stationary,
        activity_type = 'printing',
        status='completed'
    ).count()

    # total editing or typing
    total_editing_typing = Activity.objects.filter(
        stationary_profile=stationary,
        activity_type = 'typing and editing',
        status='completed'
    ).count()

    return render(request, "stationary/dashboard.html", {
        "total_earn": total_earn,
        "total_activity": total_activities,
        "bonus": bonus,

        # total activities based on type
        "printing": total_printing,
        "editing_or_typing": total_editing_typing
    })