# vim: ts=4:sw=4:expandtabs

__author__ = 'zach.mott@gmail.com'

from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class CreateAccountForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    confirm = forms.CharField()

    def clean(self):
        cleaned_data = super(CreateAccountForm, self).clean()

        if cleaned_data['password'] != cleaned_data['confirm']:
            msg = _("'password' and 'confirm' fields must match.")
            raise ValidationError(msg)

        return cleaned_data
