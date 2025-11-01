from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.conf import settings


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'LogingUserSystem/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'LogingUserSystem/login.html', {'form': form})



def logout(request):
    auth_logout(request)
    return redirect('login')

def delete_test_user(request):
    if settings.DEBUG and request.GET.get("username"):
        User.objects.filter(username=request.GET["username"]).delete()
        return JsonResponse({"status": "deleted"})
    return JsonResponse({"error": "not allowed"}, status=403)