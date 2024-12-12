from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Driver
from .forms import DriverForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# @login_required
def driver_list(request):
    drivers = Driver.objects.all().order_by('id')
    paginator = Paginator(drivers, 15)

    page_number = request.GET.get('page', 1)

    drivers_page = paginator.get_page(page_number)

    drivers_data = list(drivers_page.object_list.values('id','name', 'license_number', 'hired_at', 'updated_at', 'assigned_vehicle'))

    # Return the data as JSON
    return JsonResponse({'drivers': drivers_data, 'page': page_number, 'total_pages': paginator.num_pages})

    # Return data as an HTML template

    # return render(request, 'drivers/driver_list.html', {'drivers': drivers_page})


@login_required
def driver_detail(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    return render(request, 'drivers/detail.html', {'driver': driver})

@login_required
def driver_create(request):
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('driver_list')
    else:
        form = DriverForm()
    return render(request, 'drivers/create.html', {'form': form})

@login_required
def driver_update(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('driver_detail', driver_id=driver.id)
    else:
        form = DriverForm(instance=driver)
    return render(request, 'drivers/update.html', {'form': form})

@login_required
def driver_delete(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == 'POST':
        driver.delete()
        return redirect('driver_list')
    return render(request, 'drivers/delete.html', {'driver': driver})
