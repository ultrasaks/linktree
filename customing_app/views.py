from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Profile, ColorScheme, Link, check_link_correct
from .forms import ProfileForm, ColorForm, LinkForm
from .decorators import profile_required, scheme_required

#TODO: перенести все <script> в js файлы
#TODO: добавить мету в показ профиля чтобы верх страницы перекрашивался в фон
import json


@login_required
def home(request):
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
    profile = Profile.objects.filter(owner=request.user).first()
    color_scheme = profile.colors
    links = Link.objects.filter(user_profile=profile)

    return render(request, 'test.html', {'scheme': color_scheme, 'profile': profile, 'links': links})



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
            color_object = form.cleaned_data["to_change"]
            color = form.cleaned_data["color"]


            if not profile.colors.check_color(color):
                to_return['message'] = 'Wrong color'
                return HttpResponse(json.dumps(to_return), status=400, content_type="application/json")
            match color_object:
                case "background":
                    scheme.background = color
                case "font":
                    scheme.font = color
                case "card":
                    scheme.card = color
                case "button":
                    scheme.button = color
                case "button_hover":
                    scheme.button_hover = color
                case "button_click":
                    scheme.button_click = color
                case "button_font":
                    scheme.button_font = color
                # case "button_outline":
                #     scheme.button_outline = color

                case _:
                    to_return['message'] = 'Wrong object'
                    return HttpResponse(json.dumps(to_return), status=400, content_type="application/json")

            scheme.save()
            to_return['message'] = 'Success!'
            return HttpResponse(json.dumps(to_return), content_type="application/json")
        else:
            to_return['message'] = "invalid"
    return HttpResponse(json.dumps(to_return), status=400, content_type="application/json")
#? TODO: удаление ссылок
@login_required
@scheme_required
def create_link(request):
    #TODO: удаление ссылки
    profile = Profile.objects.filter(owner=request.user).first()
    form = LinkForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        url = cd['url']
        title = cd['title']
        icon = cd['icon']
        past_id = cd['edit_id']
        if icon not in settings.BRAND_ICONS:
            icon = 'link'
        
        if not check_link_correct(url):
            return HttpResponse('oksimiron', status=400)
        
        if past_id is None:
            link = Link(icon=icon, url=url, title=title, user_profile=profile)
            link.save()
        else:
            link = Link.objects.filter(id=past_id).first()
            if link is None:
                return HttpResponse('oksimiron', status=400)
            
            link.url = url
            link.title = title
            link.icon = icon
            link.save()
        return HttpResponse(json.dumps({'status': 'OK', 'id': link.id}), content_type="application/json")
    return HttpResponse('oksimiron', status=400)


# def search_icon(request):
#     BRAND_ICONS

# яркость определяется по HSV(v)
#TODO: перенести все style= <style> <script> в css и js файлы соответственно