from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from stationary_system.models.stationary import StationaryProfile
from stationary_system.models.payments import Payments

# payment list
@login_required(login_url='login_page_stationary') 
def payments_list(request):
    stationary = StationaryProfile.objects.filter(user=request.user).first()

    if not stationary:
        payments = []
    else:
        payments = Payments.objects.select_related('user').filter(
            stationary_profile=stationary
        ).order_by('-paid_at')

    return render(request, "stationary/payments.html", {
        "payments": payments
    })


# delete all payment history
@login_required(login_url='login_page_stationary') 
def delete_all_payments(request):
    stationary = StationaryProfile.objects.filter(user=request.user).first()

    if not stationary:
        return redirect('stationary_payments')

    Payments.objects.filter(stationary_profile=stationary).delete()

    return redirect('stationary_payments')