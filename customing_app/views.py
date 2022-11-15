from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Profile, Link
from .decorators import profile_required, scheme_required


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
    #TODO: сделать более похожим на links_edit
    profile = Profile.objects.filter(owner=request.user).first()
    color_scheme = profile.colors
    return render(request, 'colors_edit.html', {'title': 'Изменение цвета', 'scheme': color_scheme})
    


@login_required
@scheme_required
def links_edit(request):
    #TODO: Фронт для мобилок - более нормальное расположение кнопок
    #? анимированное
    profile = Profile.objects.filter(owner=request.user).first()
    links = Link.objects.filter(user_profile=profile)
    all_icons = settings.NO_BRAND
    return render(request, 'links_edit.html', {'title': 'Изменение цвета', 'links': links, 'all_icons': all_icons})

@login_required
@scheme_required
def link_test(request):
    #TODO: то же самое но с верхней штукой
    return redirect(f'/l/{request.user.username}')


#TODO: перенести все style= <style> <script> в css и js файлы соответственно