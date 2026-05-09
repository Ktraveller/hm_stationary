from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from stationary_system.models.payments import Payments

# payment list
@login_required(login_url='login_page_admin') 
def payments_list(request):
    payments = Payments.objects.select_related('user').order_by('-paid_at')

    return render(request, "admin/payments.html", {
        "payments": payments
    })


# delete all payment history
@login_required(login_url='login_page_admin') 
def delete_all_payments(request):
    payments = Payments.objects.all()
    payments.delete()
    return render(request, "admin/payments.html")