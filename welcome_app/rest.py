from django.shortcuts import HttpResponse

from json import loads, dumps

from .forms import RegisterP1Form 
from .models import User


def register_part_1(request):
    form = RegisterP1Form(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if User.objects.filter(email=cd['email']).first() is not None:
            return HttpResponse(dumps({'status': 0}), content_type="application/json")
        elif User.objects.filter(username=cd['username']).first() is not None:
            return HttpResponse(dumps({'status': 1}), content_type="application/json")
        
        return HttpResponse(dumps({'status': 'success'}), content_type="application/json")
    return HttpResponse(dumps({'status': 2}), content_type="application/json")
    