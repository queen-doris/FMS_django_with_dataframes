import json
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from vehicles.models import Vehicle
from drivers.models import Driver
from django.db.models.functions import TruncMonth
from django.db.models import Count

def landing(request):
    return render(request, 'landing.html')

@login_required
def home(request):
    # Query dynamic data for the chart
    vehicle_count = Vehicle.objects.count()
    driver_count = Driver.objects.count()

    # Monthly data aggregation using TruncMonth
    monthly_vehicle_data = (
        Vehicle.objects.annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    monthly_driver_data = (
        Driver.objects.annotate(month=TruncMonth('hired_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Prepare data for Chart.js
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    vehicle_data = [0] * 12
    driver_data = [0] * 12

    for record in monthly_vehicle_data:
        vehicle_data[record['month'].month - 1] = record['count']

    for record in monthly_driver_data:
        driver_data[record['month'].month - 1] = record['count']

    context = {
        'username': request.user.username,
        'months': json.dumps(months),
        'vehicle_data': json.dumps(vehicle_data),
        'driver_data': json.dumps(driver_data),
    }
    return render(request, 'base.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.info(request, f'Account created for {username}!')
            return redirect('login')  # Redirect to login after signup
    else:
        form = UserCreationForm()
    return render(request, 'authapp/signup.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

def session_timeout_middleware(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            now = timezone.now()

            # Check session timeout
            if last_activity:
                try:
                    last_activity_time = timezone.datetime.fromisoformat(last_activity)
                    if now - last_activity_time > timedelta(minutes=10):  # Set to 10 minutes
                        logout(request)
                        messages.warning(request, "You have been logged out due to inactivity.")
                        return redirect('login')
                except ValueError:
                    # If parsing fails, log out the user as a safeguard
                    logout(request)
                    return redirect('login')

            # Update session activity timestamp
            request.session['last_activity'] = now.isoformat()
        return get_response(request)

    return middleware
