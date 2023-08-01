from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from customing_app.decorators import scheme_required
from customing_app.models import Profile, Link
from welcome_app.models import User

# Create your views here.
def link_show(request, alias:str=None, is_widget=False):
    if alias is None:
        return render(request, 'base.html', {'title': 'Not found'}) #404
    alias = alias.lower()
    
    owner = User.objects.filter(username=alias).first()
    if owner is None:
        return render(request, 'base.html', {'title': 'Not found'}) #404
    
    profile = Profile.objects.filter(owner=owner).first()
    if profile:
        color_scheme = profile.colors
        links = Link.objects.filter(user_profile=profile).order_by('position')
        if color_scheme is not None and links is not None:
            response = render(request, 'test.html', {'scheme': color_scheme, 'profile': profile, 'links': links, 'widget': is_widget})
            response['X-Frame-Options'] = 'ALLOWALL'
            return response
    return render(request, 'base.html', {'title': 'Not found'}) #404