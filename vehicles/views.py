from django.shortcuts import render, redirect, get_object_or_404
from .models import Vehicle
from .forms import VehicleForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse

# @login_required
def home(request):
    vehicles = Vehicle.objects.all()  # Fetch all vehicles from the database
    return render(request, 'base.html', {'vehicles': vehicles})

# @login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.all().order_by('id')

    paginator = Paginator(vehicles, 15)

    page_number = request.GET.get('page', 1)

    vehicles_page = paginator.get_page(page_number)

# Return the data as JSON
    return JsonResponse({'vehicles': list(vehicles_page.object_list.values('id','name', 'license_plate', 'vehicle_type', 'created_at')), 'page': page_number, 'total_pages': paginator.num_pages})

# Return data with an HTML template

# return render(request, 'vehicles/vehicle_list.html', {"vehicles": vehicles_page})

@login_required
def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')   
    else:
        form = VehicleForm()
    return render(request, 'vehicles/create_vehicle.html', {'form': form})


@login_required
def update_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'vehicles/update_vehicle.html', {'form': form})

@login_required
def delete_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('vehicle_list')
    return render(request, 'vehicles/delete_vehicle.html', {'vehicle': vehicle})
