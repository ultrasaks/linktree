from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Profile, ColorScheme, Link, check_link_correct
from .forms import ProfileForm, ColorForm, LinkForm
from .decorators import profile_required, scheme_required

#TODO: перенести все <script> в js файлы
#TODO: добавить <meta> в показ профиля чтобы верх страницы перекрашивался в фон


@login_required
def home(request):
    #TODO: добавить изменение ника, ссылки
    profile = Profile.objects.filter(owner=request.user).first()
    return render(request, 'home.html', {'title': 'Настройка профиля', 'profile': profile})


@login_required
@scheme_required
def links(request):
    profile = Profile.objects.filter(owner=request.user).first()
    links = Link.objects.filter(user_profile=profile)
    return render(request, 'links.html', {'title': 'Настройка ссылок', 'links': links})


@login_required
@profile_required
def colors(request):
    profile = Profile.objects.filter(owner=request.user).first()
    color_scheme = profile.colors
    return render(request, 'colors.html', {'title': 'Настройка дизайна', 'scheme': color_scheme})


@login_required
@scheme_required
def colors_edit(request):
    profile = Profile.objects.filter(owner=request.user).first()
    color_scheme = profile.colors
    return render(request, 'colors_edit.html', {'title': 'Изменение цвета', 'scheme': color_scheme})
    


@login_required
@scheme_required
def links_edit(request):
    #TODO: Кнопка изменения ссылок, добавление этой кнопки после создания ссылки
    #TODO: Показывать название ссылки без brand-
    profile = Profile.objects.filter(owner=request.user).first()
    links = Link.objects.filter(user_profile=profile)
    all_icons = settings.BRAND_ICONS
    return render(request, 'links_edit.html', {'title': 'Изменение цвета', 'links': links, 'all_icons': all_icons})


@login_required
@scheme_required
def link_test(request):
    #TODO: перенести в show_app
    profile = Profile.objects.filter(owner=request.user).first()
    color_scheme = profile.colors
    links = Link.objects.filter(user_profile=profile)

    return render(request, 'test.html', {'scheme': color_scheme, 'profile': profile, 'links': links})


#TODO: перенести все style= <style> <script> в css и js файлы соответственно