from django.shortcuts import render, get_object_or_404, redirect
from .models import Soldier, FamilyMember, StatusHistory, EmergencyContact
from .forms import SoldierForm, FamilyLinkForm, AdminFamilyLinkForm, EmergencyContactForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.db import models
from accounts.models import CustomUser
from missions.models import SoldierMission


@login_required
def soldier_list(request: HttpRequest) -> HttpResponse:
    soldiers = Soldier.objects.all()
    return render(request, 'view/list.html',{'soldiers': soldiers})

@login_required
def soldier_detail(request: HttpRequest, pk: int) -> HttpResponse:
    soldier = get_object_or_404(Soldier, pk=pk)
    family_links = FamilyMember.objects.filter(soldier=soldier, is_active=True)
    return render(request, 'view/detail.html', {'soldier': soldier, 'family_links': family_links})

@login_required
def soldier_create(request):
    if request.method == 'POST':
        form = SoldierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('soldier_list')
    else:
        form = SoldierForm()
    return render(request, 'view/create.html', {'form': form})

@login_required
def soldier_update(request, pk):
    soldier = get_object_or_404(Soldier, pk=pk)
    
    if request.user.role != 'admin':
        return redirect('soldier_detail', pk=pk)

    if request.method == 'POST':
        form = SoldierForm(request.POST, instance=soldier)
        if form.is_valid():
            soldier = form.save(commit=False)
            soldier.updated_by = request.user  # Inject the user into the model
            soldier.save()
            return redirect('soldier_detail', pk=pk)
    else:
        form = SoldierForm(instance=soldier)
    return render(request, 'view/update.html', {'form': form})


@login_required
def family_dashboard(request):
    if request.user.role != 'family':
        return redirect('home')

    family_links = FamilyMember.objects.filter(user=request.user).select_related('soldier')
    linked_soldiers = [link.soldier for link in family_links]
    
    mission_data = {
        soldier.pk: SoldierMission.objects.filter(soldier=soldier).select_related('mission')
        for soldier in linked_soldiers
    }

    return render(request, 'view/family_dashboard.html', {
        'family_links': family_links,
        'soldiers': linked_soldiers,
        'mission_data': mission_data

    })
@login_required
def soldier_status_history(request, pk):
    soldier = get_object_or_404(Soldier, pk=pk)

    if request.user.role == 'family':
        if not FamilyMember.objects.filter(user=request.user, soldier=soldier, is_active=True).exists():
            return redirect('family_dashboard')
        
    history = StatusHistory.objects.filter(soldier=soldier).order_by('-status_date')
    return render(request, 'view/status_history.html', {
        'soldier': soldier,
        'history': history
    })


@login_required
def soldier_list(request):
    query = request.GET.get('q')
    soldiers = Soldier.objects.all()

    if query:
        soldiers = soldiers.filter(
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query) |
            models.Q(service_id__icontains=query)
        )

    return render(request, 'view/list.html', {
        'soldiers': soldiers,
        'query': query
    })

@login_required
def soldier_home(request):
    if request.user.role != 'admin':
        raise PermissionDenied
    return render(request, 'view/soldier.html', {})


@login_required
def link_to_soldier(request):
    if request.user.role != 'family':
        return redirect('home')

    query = request.GET.get('q', '')
    form = FamilyLinkForm(request.POST or None, user=request.user)

    soldiers = Soldier.objects.exclude(
        id__in=FamilyMember.objects.filter(user=request.user).values_list('soldier_id', flat=True)
    )
    if query:
        soldiers = soldiers.filter(
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query) |
            models.Q(service_id__icontains=query)
        )

    if request.method == 'POST' and form.is_valid():
        soldier_id = request.POST.get('soldier')
        try:
            soldier = Soldier.objects.get(id=soldier_id)
        except Soldier.DoesNotExist:
            form.add_error('soldier', 'Invalid soldier selected.')
        else:
            existing = FamilyMember.objects.filter(user=request.user, soldier=soldier)
            if not existing.exists():
                family_link = form.save(commit=False)
                family_link.user = request.user
                family_link.soldier = soldier
                family_link.save()
                messages.success(request, "You are now linked to this soldier.")
                return redirect('family_dashboard')
            else:
                form.add_error(None, 'You are already linked to this soldier.')

    return render(request, 'linking/family_link.html', {
        'form': form,
        'query': query,
        'soldiers': soldiers,
    })



@login_required
def unlink_soldier(request, pk):
    link = get_object_or_404(FamilyMember, pk=pk, user=request.user)
    if request.method == 'POST':
        link.delete()
        messages.success(request, "You have unlinked from the soldier.")
        return redirect('family_dashboard')
    return render(request, 'linking/unlink_confirm.html', {'link': link})


def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@user_passes_test(is_admin)
def admin_link_family(request):
    soldier_query = request.GET.get('soldier_q', '')
    user_query = request.GET.get('user_q', '')

    soldiers = Soldier.objects.all()
    users = CustomUser.objects.filter(role='family', is_active=True)

    if soldier_query:
        soldiers = soldiers.filter(
            models.Q(first_name__icontains=soldier_query) |
            models.Q(last_name__icontains=soldier_query) |
            models.Q(service_id__icontains=soldier_query)
        )

    if user_query:
        users = users.filter(
            models.Q(first_name__icontains=user_query) |
            models.Q(last_name__icontains=user_query) |
            models.Q(email__icontains=user_query)
        )

    if request.method == 'POST':
        form = AdminFamilyLinkForm(request.POST, soldiers_queryset=soldiers, users_queryset=users)
        if form.is_valid():
            form.save()
            messages.success(request, "Family member linked successfully.")
            return redirect('soldier_list')
    else:
        form = AdminFamilyLinkForm(soldiers_queryset=soldiers, users_queryset=users)

    return render(request, 'linking/admin_link_family.html', {
        'form': form,
        'soldier_query': soldier_query,
        'user_query': user_query,
    })


@login_required
def add_emergency_contact(request, soldier_id):
    soldier = get_object_or_404(Soldier, pk=soldier_id)
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.soldier = soldier

            if contact.is_primary:
                # Unmark all other primary contacts
                EmergencyContact.objects.filter(soldier=soldier, is_primary=True).update(is_primary=False)

            contact.save()
            messages.success(request, 'Emergency contact added successfully.')
            return redirect('soldier_detail', pk=soldier.pk)
    else:
        form = EmergencyContactForm()
    return render(request, 'view/emergency_contact.html', {'form': form, 'soldier': soldier})


@login_required
def delete_emergency_contact(request, contact_id):
    contact = get_object_or_404(EmergencyContact, pk=contact_id)
    
    if request.user.role != 'admin':
        messages.error(request, 'Only admins can delete emergency contacts.')
        return redirect('soldier_detail', pk=contact.soldier.pk)

    soldier_id = contact.soldier.pk
    contact.delete()
    messages.success(request, 'Emergency contact deleted.')
    return redirect('soldier_detail', pk=soldier_id)

@login_required
def edit_emergency_contact(request, contact_id):
    contact = get_object_or_404(EmergencyContact, pk=contact_id)

    # Optional: restrict access — family can only edit their linked soldier’s contact
    if request.user.role == 'family':
        if not FamilyMember.objects.filter(user=request.user, soldier=contact.soldier).exists():
            return redirect('profile')

    if request.method == 'POST':
        form = EmergencyContactForm(request.POST, instance=contact)
        if form.is_valid():
            updated_contact = form.save(commit=False)

            if updated_contact.is_primary:
                EmergencyContact.objects.filter(soldier=contact.soldier, is_primary=True).exclude(pk=contact.pk).update(is_primary=False)

            updated_contact.save()
            messages.success(request, 'Contact updated.')
            return redirect('soldier_detail', pk=contact.soldier.pk)
    else:
        form = EmergencyContactForm(instance=contact)

    return render(request, 'view/emergency_contact.html', {'form': form, 'soldier': contact.soldier})

@login_required
def family_emergency_contacts(request):
    if request.user.role != 'family':
        return redirect('profile')

    links = FamilyMember.objects.filter(user=request.user, is_active=True)
    contacts_by_soldier = {
        link.soldier: link.soldier.emergency_contacts.all() for link in links
    }

    return render(request, 'view/family_emergency.html', {
        'contacts_by_soldier': contacts_by_soldier
    })
