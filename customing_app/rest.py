from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .decorators import profile_required, scheme_required
from .models import Profile, ColorScheme, Link, check_link_correct
from .forms import ProfileForm, ColorForm, LinkForm, DeleteLinkForm

import json


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
@profile_required
def create_scheme(request):
    to_return = {}

    profile = Profile.objects.filter(owner=request.user).first()
    if profile.colors is not None:
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
@scheme_required
def edit_scheme(request):
    to_return = {}

    profile = Profile.objects.filter(owner=request.user).first()
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

            case _:
                to_return['message'] = 'Wrong object'
                return HttpResponse(json.dumps(to_return), status=400, content_type="application/json")

        scheme.save()
        to_return['message'] = 'Success!'
        return HttpResponse(json.dumps(to_return), content_type="application/json")
    else:
        to_return['message'] = "invalid"
    return HttpResponse(json.dumps(to_return), status=400, content_type="application/json")


@login_required
@scheme_required
def create_link(request):
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


@login_required
@scheme_required
def delete_link(request):
    profile = Profile.objects.filter(owner=request.user).first()
    form = DeleteLinkForm(request.POST)
    
    if form.is_valid():
        link_id = form.cleaned_data['id']
        to_delete = Link.objects.filter(id=link_id, user_profile=profile).first()
        if to_delete is not None:
            to_delete.delete()
            return HttpResponse('OK')
    return HttpResponse('oksimiron', status=400)

# def search_icon(request):
#     settings.BRAND_ICONS

# яркость определяется по HSV(v)