from django.shortcuts import render, HttpResponse


def home(request):
    return HttpResponse('Hello friend')

# яркость определяется по HSV(v)