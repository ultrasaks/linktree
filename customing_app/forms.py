from django import forms


class ProfileForm(forms.Form):
    username = forms.CharField()
    about = forms.CharField()