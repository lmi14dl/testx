from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomAuthenticationForm, CustomUserCreationForm, UpdateUserForm, CustomPasswordChangeForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


def signup_view(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password1)
            login(request, user)
            messages.success(request, "Your account has created")
            return redirect('home')
        return render(request, "users/signup.html", {'form': form})
    else:
        return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You've logged in to your account successfully")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return render(request, "users/login.html", {'form': form})
    else:
        form = CustomAuthenticationForm()
    return render(request, "users/login.html", {'form':form})


def logout_view(request):
    logout(request)
    messages.success(request, "You've logged out from your account!")
    return redirect('home')


def update_user_view(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Your profile was updated successfully")
            return render(request, "users/update_user.html", {'user_form': user_form})
        return render(request, "users/update_user.html", {'user_form':user_form})
    else:
        messages.success(request, "First you have to login to your account")
        return redirect('home')
    


def change_password_view(request):
    if request.user.is_authenticated:
        current_user = request.user
        
        if request.method == 'POST':
            form = CustomPasswordChangeForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password changed successfully')
                update_session_auth_hash(request, current_user)
                return render(request, "users/update_user.html", {'form': form})
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return render(request, 'users/change_password.html', {'form': form})
        else:
            form = CustomPasswordChangeForm(current_user)
        return render(request, 'users/change_password.html', {'form':form})
    else:
        messages.success(request, "First you have to login to your account.")
        return redirect('login')