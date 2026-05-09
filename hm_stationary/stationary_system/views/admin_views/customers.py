from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import Group

from stationary_system.models.accounts import CustomUser


# customer list
@login_required(login_url='login_page_admin') 
def admin_customers(request):
    search_query = request.GET.get('search', '')

    # Get the 'Customer' group
    customer_group = Group.objects.get(name='customer')

    # Filter users who belong to the Customer group
    customers = CustomUser.objects.filter(groups=customer_group).order_by('id')

    # Apply search filter (username, email, phone)
    if search_query:
        customers = customers.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    return render(request, 'admin/customers.html', {
        'customers': customers,
        'search_query': search_query,
    })



@login_required(login_url='login_page_admin') 
def preview_customer(request, user_id):
    customer = get_object_or_404(CustomUser, id=user_id)

    return render(request, 'admin/customer.html', {
        'customer': customer
    })