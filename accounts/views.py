from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserEditForm, CustomPasswordChangeForm
from django.contrib import messages
from .models import CustomUser
from django.http import HttpRequest

def register_view(request: HttpRequest):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'views/register.html', {'form': form})

def login_view(request: HttpRequest):
    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)
        
        if login_form.is_valid():
            login(request, login_form.get_user())
            return redirect('profile')
    else:
        login_form = AuthenticationForm()
    return render(request, 'views/login.html', {'login_form': login_form})



def logout_view(request: HttpRequest):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request: HttpRequest):
    return render(request, 'views/profile.html', {'user': request.user})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # log them out first
        user.delete()    # then delete account
        messages.success(request, "Your account has been deleted.")
        return redirect('home')  # or 'login' if preferred
    return render(request, 'views/delete_account.html')

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = CustomUserEditForm(instance=request.user)

    return render(request, 'views/edit_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfully.')
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'password/password_change.html', {'form': form})