from django import forms


class ProfileForm(forms.Form):
    name = forms.CharField(max_length=100)
    about = forms.CharField(max_length=400)


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


class ChangeColorForm(forms.Form):
    color_id = forms.CharField()
    color_hash = forms.CharField(max_length=8)


class ChangeButtonForm(forms.Form):
    button_id = forms.CharField(max_length=4)


class ChangeFontForm(forms.Form):
    font_name = forms.CharField()