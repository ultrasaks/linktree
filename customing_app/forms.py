from django import forms


class ProfileForm(forms.Form):
    username = forms.CharField()
    about = forms.CharField()


class ColorForm(forms.Form):
    to_change = forms.CharField()
    color = forms.CharField()