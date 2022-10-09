from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required

from .models import Profile, ColorScheme
from .forms import ProfileForm

import json

@login_required
def home(request):
    profile = Profile.objects.filter(owner=request.user).first()
    return render(request, 'home.html', {'title': 'Настройка профиля', 'profile': profile})


@login_required
def links(request):
    profile = Profile.objects.filter(owner=request.user).first()
    if profile is None:
        return redirect('/')
    # if profile.colors is None:
    #     return redirect('/profile/colors/')
    return render(request, 'links.html', {'title': 'Настройка ссылок'})


@login_required
def colors(request):
    profile = Profile.objects.filter(owner=request.user).first()
    if profile is None:
        return redirect('/')
    color_scheme = ColorScheme.objects.filter(owner=profile).first()
    return render(request, 'colors.html', {'title': 'Настройка дизайна', 'scheme': color_scheme})



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

    


# яркость определяется по HSV(v)