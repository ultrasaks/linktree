from django import forms


class ProfileForm(forms.Form):
    username = forms.CharField()
    about = forms.CharField()


class ColorForm(forms.Form):
    to_change = forms.CharField()
    color = forms.CharField()


class LinkForm(forms.Form):
    icon = forms.CharField()
    url = forms.CharField()
    title = forms.CharField()
    edit_id = forms.IntegerField(required=False)