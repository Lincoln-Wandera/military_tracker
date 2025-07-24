from django.shortcuts import render, get_object_or_404, redirect
from .models import Mission, SoldierMission
from .forms import MissionForm, SoldierMissionForm
from django.contrib.auth.decorators import login_required

# Mission CRUD
@login_required
def mission_list(request):
    missions = Mission.objects.all()
    return render(request, 'mission/list.html', {'missions': missions})

@login_required
def mission_detail(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    assignments = SoldierMission.objects.filter(mission=mission)
    return render(request, 'mission/detail.html', {'mission': mission, 'assignments': assignments})

@login_required
def mission_create(request):
    if request.method == 'POST':
        form = MissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mission_list')
    else:
        form = MissionForm()
    return render(request, 'mission/create.html', {'form': form})

@login_required
def mission_update(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    if request.method == 'POST':
        form = MissionForm(request.POST, instance=mission)
        if form.is_valid():
            form.save()
            return redirect('mission_detail', pk=pk)
    else:
        form = MissionForm(instance=mission)
    return render(request, 'mission/update.html', {'form': form})

# Soldier Assignment
@login_required
def assign_soldier(request):
    if request.method == 'POST':
        form = SoldierMissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mission_list')
    else:
        form = SoldierMissionForm()
    return render(request, 'mission/assign_soldier.html', {'form': form})

@login_required
def mission_home(request):
    if request.user.role != 'admin':
        raise PermissionDenied
    return render(request, 'mission/mission.html', {})