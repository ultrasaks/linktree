from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import ProfileForm

import json

@login_required
def home(request):
    profile = Profile.objects.filter(owner=request.user)
    return render(request, 'home.html', {'title': 'Настройка профиля', 'profile': profile})


@login_required
def links(request):
    if not Profile.objects.filter(owner=request.user):
        return redirect('/')
    return render(request, 'home.html', {'title': 'Настройка ссылок'})



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