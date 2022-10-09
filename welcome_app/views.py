from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegisterForm


def form_error(form) -> str:
    return form.errors.as_data()[list(form.errors.keys())[0]][0].message

def form_error_name(form) -> str:
    return list(form.errors.keys())[0]


def home(request):
    if request.user.is_authenticated:
        return redirect('/profile')
    return render(request, 'landing.html', {'title': 'MYLink'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    message = None

    if request.method == 'POST':
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if 'next' not in request.GET:
                        return redirect('/')
                    return redirect(request.GET['next'])
                else:
                    message = 'Данный аккаунт заблокирован.'
            else:
                message = 'Неправильный логин или пароль'
        else:
            message = f'{form_error_name(user_form)}: {form_error(user_form)}'
    user_form = LoginForm()
    return render(request, 'login.html', {'title': 'Вход', 'user_form': user_form, 'errors': message})


def register_view(request):
    #TODO: Капча
    if request.user.is_authenticated:
        return redirect('/')
    message = None
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('/login')
        else:
            message = f'{form_error_name(user_form)}: {form_error(user_form)}'
    user_form = RegisterForm()
    return render(request, 'signup.html', {'title': 'Регистрация', 'user_form': user_form, 'errors': message})


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')