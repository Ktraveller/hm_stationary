from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login_page_stationary') 
def notifications(request):
  return render(request, 'stationary/notifications.html')

@login_required(login_url='login_page_stationary') 
def user(request):
  return render(request, 'stationary/user.html')
