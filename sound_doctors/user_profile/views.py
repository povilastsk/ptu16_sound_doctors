from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import HttpRequest
from . import models, forms

User = get_user_model()

@csrf_protect
def profile_update(request: HttpRequest):
    if request.method == "POST":
        user_form = forms.UserUpdateForm(request.POST, instance=request.user)
        profile_form = forms.ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your user profile changes have been saved.')
            return redirect('profile')
    else:
        user_form = forms.UserUpdateForm(instance=request.user)
        profile_form = forms.ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'user_profile/update.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


def profile(request: HttpRequest):
    return render(request, "user_profile/profile.html")


@csrf_protect
def signup(request: HttpRequest):
    if request.method == "POST":
        errors = []
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not len(username) > 3 or User.objects.filter(username=username).exists():
            errors.append('Username is already taken, or is too short.')
        if not len(email) > 0 or User.objects.filter(email=email).exists():
            errors.append('Email must be valid and not belonging to existing user.')
        if not len(password1) > 7 or password1 != password2:
            errors.append('Password is too short, or entered passwords do not match.')
        if len(errors):
            for error in errors:
                messages.error(request, error)
        else:
            User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, "Sign up successful. You can login now.")
            return redirect('login')
    return render(request, 'user_profile/signup.html')
