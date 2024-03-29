from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User
import re

PASSWORD_REGEX = '((?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{6,})'


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterP1Form(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=400)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Пароли не совпадают.")
        if re.search(PASSWORD_REGEX, cd['password']) is None:
            raise forms.ValidationError("Пароль не содержит одного из перечисленных символов")
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email',)


class CUserRegForm(RegisterForm):
    class Meta:
        model = User
        fields = ('email', 'username',)


class CUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username',)


