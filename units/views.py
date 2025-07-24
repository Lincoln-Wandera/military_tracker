from django.shortcuts import render, get_object_or_404, redirect
from .models import Unit
from .forms import UnitForm
from django.contrib.auth.decorators import login_required

@login_required
def unit_list(request):
    units = Unit.objects.all()
    return render(request, 'tem/list.html', {'units': units})

@login_required
def unit_detail(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    return render(request, 'tem/details.html', {'unit': unit})

@login_required
def unit_create(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('unit_list')
    else:
        form = UnitForm()
    return render(request, 'tem/create.html', {'form': form})

@login_required
def unit_update(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('unit_detail', pk=pk)
    else:
        form = UnitForm(instance=unit)
    return render(request, 'tem/update.html', {'form': form})

@login_required
def unit_home(request):
    if request.user.role != 'admin':
        raise PermissionDenied
    return render(request, 'tem/unit.html', {}) 