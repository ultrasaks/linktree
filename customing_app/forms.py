from django import forms


class ProfileForm(forms.Form):
    username = forms.CharField()
    about = forms.CharField()


class ColorForm(forms.Form):
    to_change = forms.CharField()
    color = forms.CharField()


class LinkEditForm(forms.Form):
    id = forms.IntegerField()
    url = forms.CharField()
    title = forms.CharField()

class LinkPosForm(forms.Form):
    id = forms.IntegerField()
    where = forms.IntegerField()


class NewLinkForm(forms.Form):
    url = forms.CharField()

class DeleteLinkForm(forms.Form):
    id = forms.IntegerField()