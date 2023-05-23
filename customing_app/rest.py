from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import F

from .decorators import profile_required, scheme_required
from .models import Profile, ColorScheme, Link, check_link_correct
from .forms import ProfileForm, ColorForm, LinkEditForm, DeleteLinkForm, NewLinkForm, LinkPosForm, ChangeColorForm, ChangeFontForm, ChangeButtonForm

from bs4 import BeautifulSoup
from requests import get
from re import compile

import json

url_pattern = compile(r'/^([a-z]+:\/\/)?([a-z0-9-]+\.)?[a-z0-9-]+\.[a-z]+(\/.*)?$/i')


@login_required
def create_profile(request):
    to_return = {}
    form = ProfileForm(json.loads(request.body))
    if form.is_valid():
        if Profile.objects.filter(owner=request.user):
            to_return['message'] = 'Your account already has a profile'
            return HttpResponse(json.dumps(to_return), status=400, content_type="application/json")
        cd = form.cleaned_data
        new_profile = Profile(name=cd['name'], about=cd['about'], owner=request.user)
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


# @login_required
# @scheme_required
# def edit_scheme(request):
#     to_return = {}

#     profile = Profile.objects.filter(owner=request.user).first()
#     form = ColorForm(request.POST)
#     if form.is_valid():
#         scheme = profile.colors
#         color_object = form.cleaned_data["to_change"]
#         color = form.cleaned_data["color"]

#         if not profile.colors.check_color(color):
#             to_return['message'] = 'Wrong color'
#             return HttpResponse(json.dumps(to_return), status=400, content_type="application/json")
        
#         match color_object:
#             case "background":
#                 scheme.background = color
#             case "font":
#                 scheme.font = color
#             case "card":
#                 scheme.card = color
#             case "button":
#                 scheme.button = color
#             case "button_hover":
#                 scheme.button_hover = color
#             case "button_click":
#                 scheme.button_click = color
#             case "button_font":
#                 scheme.button_font = color

#             case _:
#                 to_return['message'] = 'Wrong object'
#                 return HttpResponse(json.dumps(to_return), status=400, content_type="application/json")

#         scheme.save()
#         to_return['message'] = 'Success!'
#         return HttpResponse(json.dumps(to_return), content_type="application/json")
#     else:
#         to_return['message'] = "invalid"
#     return HttpResponse(json.dumps(to_return), status=400, content_type="application/json")


@login_required
@scheme_required
def create_link(request):
    profile = Profile.objects.filter(owner=request.user).first()
    form = NewLinkForm(json.loads(request.body))
    if form.is_valid():
        url = form.cleaned_data['url']
        
        if not check_link_correct(url):
            return HttpResponse('oksimiron', status=400)
        
        title, icon = get_title_icon(url)
        
        link = Link(icon=icon, url=url, title=title, user_profile=profile)
        link.save()
        return HttpResponse(json.dumps([link.id, link.url, link.title, link.position]), content_type="application/json")
        
    return HttpResponse('oksimiron', status=400)


@login_required
@scheme_required
def edit_link_name(request):
    form = LinkEditForm(json.loads(request.body))
    if form.is_valid():
        cd = form.cleaned_data
        link_id = cd['id']
        url = cd['url']
        title = cd['title']
        
        link = Link.objects.filter(id=link_id).first()
        if link is None:
            return HttpResponse('oksimiron', status=400)
        
        link.url = url
        link.title = title
        link.save()
        
        return HttpResponse('Success', status=200)
    
    
@login_required
@scheme_required
def edit_pos(request):
    form = LinkPosForm(json.loads(request.body))
    if form.is_valid():
        cd = form.cleaned_data
        link_id = cd['id']
        where = cd['where']
        
        link = Link.objects.filter(id=link_id).first()
        if link is None:
            return HttpResponse('oksimiron', status=400)
        
        if not where:
            link2 = Link.objects.filter(position=link.position-1).first()
        else:
            link2 = Link.objects.filter(position=link.position+1).first()
        
        
        link.position, link2.position = link2.position, link.position
        link.save()
        link2.save()
        
        return HttpResponse('Success', status=200)


def get_title_icon(url:str) -> tuple:
    try:
        get_url = url if url[:4].lower() == 'http' else f'http://{url}'
        response = get(get_url)
    except:
        return (url, 'link')
    if response.status_code != 200:
        return (url, 'link')
    
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string
    
    # icon = 
    return (title, 'link')


@login_required
@scheme_required
def delete_link(request):
    profile = Profile.objects.filter(owner=request.user).first()
    cd = json.loads(request.body)
    form = DeleteLinkForm(cd)
    
    if form.is_valid():
        link_id = form.cleaned_data['id']
        to_delete = Link.objects.filter(id=link_id, user_profile=profile).first()
        if to_delete is not None:
            for link in Link.objects.filter(position__gt=to_delete.position).all():
                link.position = link.position - 1
                link.save()

            to_delete.delete()
            return HttpResponse('OK')
    return HttpResponse('oksimiron', status=400)


@login_required
@scheme_required
def change_color(request):
    scheme = Profile.objects.filter(owner=request.user).first().colors
    cd = json.loads(request.body)
    form = ChangeColorForm(cd)

    if form.is_valid():
        cd = form.cleaned_data
        if scheme.set_color(cd['color_id'], cd['color_hash']):
            return HttpResponse('OK')
    return HttpResponse('oksimiron', status=400)


@login_required
@scheme_required
def change_font(request):
    scheme = Profile.objects.filter(owner=request.user).first().colors
    cd = json.loads(request.body)
    form = ChangeColorForm(cd)

    if form.is_valid():
        cd = form.cleaned_data
        if scheme.set_font(cd['font_name']):
            return HttpResponse('OK')
    return HttpResponse('oksimiron', status=400)


@login_required
@scheme_required
def change_button(request):
    scheme = Profile.objects.filter(owner=request.user).first().colors
    cd = json.loads(request.body)
    form = ChangeButtonForm(cd)

    if form.is_valid():
        cd = form.cleaned_data
        button = cd['button_id']
        if len(button) == 4:
            if button[0] == 's' and button[1].isdigit() and button[2] == '-' and button[3].isdigit():
                scheme.button_type = int(button[1])
                scheme.button_shape = int(button[3])
                scheme.save()
                return HttpResponse('OK')
    return HttpResponse('oksimiron', status=400)


@profile_required
def edit_profile(request):
    profile = Profile.objects.filter(owner=request.user).first()
    cd = json.loads(request.body)
    form = ProfileForm(cd)

    if form.is_valid():
        cd = form.cleaned_data
        profile.name = cd['name']
        profile.about = cd['about']
        profile.save()
        return HttpResponse('OK')
    return HttpResponse('oksimiron', status=400)

# def search_icon(request):
#     settings.BRAND_ICONS

# яркость определяется по HSV(v)


# ENTITIES = {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&apos;"}
# def make_safe(string) -> str:
#     for key, value in ENTITIES.items():
#         string = string.replace(key, value)
#     return string