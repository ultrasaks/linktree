from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required

from .models import Profile, ColorScheme
from .forms import ProfileForm, ColorForm
from .decorators import profile_required, scheme_required

import json


@login_required
def home(request):
    profile = Profile.objects.filter(owner=request.user).first()
    return render(request, 'home.html', {'title': 'Настройка профиля', 'profile': profile})


@login_required
@scheme_required
def links(request):
    # profile = Profile.objects.filter(owner=request.user).first()
    return render(request, 'links.html', {'title': 'Настройка ссылок'})


@login_required
@profile_required
def colors(request):
    profile = Profile.objects.filter(owner=request.user).first()
    color_scheme = profile.colors
    return render(request, 'colors.html', {'title': 'Настройка дизайна', 'scheme': color_scheme})


@login_required
@scheme_required
def colors_edit(request):
    # !!!TODO: пофиксить color_name
    profile = Profile.objects.filter(owner=request.user).first()
    color_scheme = profile.colors
    return render(request, 'colors_edit.html', {'title': 'Изменение цвета', 'scheme': color_scheme})
    


@login_required
@scheme_required
def link_test(request):
    urls_test = ['' for _ in range(10)]

    profile = Profile.objects.filter(owner=request.user).first()
    color_scheme = profile.colors

    return render(request, 'test.html', {'scheme': color_scheme, 'profile': profile, 'urls': urls_test})



#TODO: перенести в REST
@login_required
def create_profile(request):
    to_return = {}
    form = ProfileForm(request.POST)
    if form.is_valid():
        if Profile.objects.filter(owner=request.user):
            to_return['message'] = 'Your account already has a profile'
            return HttpResponse(json.dumps(to_return), status=400, content_type="application/json")
        cd = form.cleaned_data
        new_profile = Profile(name=cd['username'], about=cd['about'], owner=request.user)
        new_profile.save()

        to_return['message'] = 'Success!'
        return HttpResponse(json.dumps(to_return), content_type="application/json")
        
    else:
        to_return['message'] = 'Non-valid data'
    return HttpResponse(json.dumps(to_return), status=400, content_type="application/json")

    
@login_required
def create_scheme(request):
    to_return = {}

    profile = Profile.objects.filter(owner=request.user).first()
    if profile is None:
        to_return['message'] = 'Your account already has a profile'
    elif profile.colors is not None:
        to_return['message'] = 'Your profile already has a color scheme'
    else:
        new_scheme = ColorScheme(owner=profile)
        new_scheme.save()
        profile.colors = new_scheme
        profile.save()

        to_return['message'] = 'Success!'
        return HttpResponse(json.dumps(to_return), content_type="application/json")
    return HttpResponse(json.dumps(to_return), status=400, content_type="application/json")



@login_required
def edit_scheme(request):
    to_return = {}

    profile = Profile.objects.filter(owner=request.user).first()
    if profile is None:
        to_return['message'] = 'Your account already has a profile'
    elif profile.colors is None:
        to_return['message'] = "Your profile don't have a color scheme"

    else:
        form = ColorForm(request.POST)
        if form.is_valid():
            scheme = profile.colors
            cd = form.cleaned_data

            match cd['to_change']:
                case "background":
                    scheme.background = cd["color"]
                case "font":
                    scheme.font = cd["color"]
                case "card":
                    scheme.card = cd["color"]
                case "button":
                    scheme.button = cd["color"]
                case "button_hover":
                    scheme.button_hover = cd["color"]
                case "button_click":
                    scheme.button_click = cd["color"]
                case "button_font":
                    scheme.button_font = cd["color"]
                # case "button_outline":
                #     scheme.button_outline = cd["color"]

                case _:
                    to_return['message'] = 'Wrong object'
                    return HttpResponse(json.dumps(to_return), status=400, content_type="application/json")

            scheme.save()
            to_return['message'] = 'Success!'
            return HttpResponse(json.dumps(to_return), content_type="application/json")
        else:
            to_return['message'] = "invalid"
    return HttpResponse(json.dumps(to_return), status=400, content_type="application/json")

# яркость определяется по HSV(v)