from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html', {'title': 'Настройка профиля'})


@login_required
def links(request):
    return render(request, 'home.html', {'title': 'Настройка профиля'})



# яркость определяется по HSV(v)