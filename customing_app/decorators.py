from django.shortcuts import redirect

from .models import Profile, ColorScheme


def profile_required(view_func):
    def _wrapped(request, *args, **kwargs):
        profile = Profile.objects.filter(owner=request.user).first()
        if profile is None:
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return _wrapped


def scheme_required(view_func):
    '''ColorScheme and Profile required'''
    def _wrapped(request, *args, **kwargs):
        profile = Profile.objects.filter(owner=request.user).first()
        if profile is None:
            return redirect('/')
        if profile.colors is None:
            return redirect('/profile/colors/')
        return view_func(request, *args, **kwargs)
    return _wrapped
