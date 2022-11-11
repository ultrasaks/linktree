from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from customing_app.decorators import scheme_required
from customing_app.models import Profile, Link
from welcome_app.models import User

# Create your views here.
def link_show(request, alias:str=None):
    if alias is None:
        return render(request, 'base.html', {'title': 'Not found'}) #404
    alias = alias.lower()
    
    owner = User.objects.filter(username=alias).first()
    if owner is None:
        return render(request, 'base.html', {'title': 'Not found'}) #404
    
    profile = Profile.objects.filter(owner=owner).first()
    if profile:
        color_scheme = profile.colors
        links = Link.objects.filter(user_profile=profile)
        if color_scheme and links:
            return render(request, 'test.html', {'scheme': color_scheme, 'profile': profile, 'links': links})
    return render(request, 'base.html', {'title': 'Not found'}) #404