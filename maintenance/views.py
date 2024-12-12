from django.shortcuts import render, get_object_or_404, redirect
from .models import Maintenance
from .forms import MaintenanceForm
from django.contrib.auth.decorators import login_required


# @login_required
def maintenance_list(request):
    maintenances = Maintenance.objects.all()
    return render(request, 'maintenance/maintenance_list.html', {'maintenances': maintenances})


@login_required
def maintenance_create(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maintenance_list')
    else:
        form = MaintenanceForm()
    return render(request, 'maintenance/maintenance_create.html', {'form': form})


@login_required
def maintenance_update(request, pk):
    maintenance = get_object_or_404(Maintenance, pk=pk)
    if request.method == 'POST':
        form = MaintenanceForm(request.POST, instance=maintenance)
        if form.is_valid():
            form.save()
            return redirect('maintenance_list')
    else:
        form = MaintenanceForm(instance=maintenance)
    return render(request, 'maintenance/maintenance_update.html', {'form': form})


@login_required
def maintenance_delete(request, pk):
    maintenance = get_object_or_404(Maintenance, pk=pk)
    if request.method == 'POST':
        maintenance.delete()
        return redirect('maintenance_list')
    return render(request, 'maintenance/maintenance_confirm_delete.html', {'maintenance': maintenance})


@login_required
def maintenance_detail(request, pk):
    maintenance = get_object_or_404(Maintenance, pk=pk)
    return render(request, 'maintenance/maintenance_detail.html', {'maintenance': maintenance})
