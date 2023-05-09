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
    links = Link.objects.filter(user_profile=profile).order_by('position')
    all_icons = settings.NO_BRAND
    return render(request, 'links_new.html', {'title': 'Изменение цвета', 'links': links, 'all_icons': all_icons, 'selected': 1})



@login_required
@profile_required
def colors(request):
    profile = Profile.objects.filter(owner=request.user).first()
    color_scheme = profile.colors
    return render(request, 'colors.html', {'title': 'Настройка дизайна', 'scheme': color_scheme, 'selected': 2})


@login_required
@scheme_required
def colors_edit(request):
    profile = Profile.objects.filter(owner=request.user).first()
    color_scheme = profile.colors
    return render(request, 'colors_edit.html', {'title': 'Изменение цвета', 'scheme': color_scheme, 'selected': 2})
    


@login_required
@scheme_required
def links_edit(request):
    profile = Profile.objects.filter(owner=request.user).first()
    links = Link.objects.filter(user_profile=profile)
    all_icons = settings.NO_BRAND
    return render(request, 'links_edit.html', {'title': 'Изменение цвета', 'links': links, 'all_icons': all_icons, 'selected': 2})

@login_required
@scheme_required
def link_test(request):
    return redirect(f'/l/{request.user.username}')
