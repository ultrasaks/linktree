from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        return redirect('/profile')
    return render(request, 'landing.html', {'title': 'MYLink'})


def login_view(request):
    return render(request, 'login.html', {'title': 'Вход'})


def register_view(request):
    return render(request, 'signup.html', {'title': 'Вход'})


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')