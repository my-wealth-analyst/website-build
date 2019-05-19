import os
from django import forms
from django.conf import settings

from django.db import models
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm

from .models import MWA_usermodel


"""
When Django is launched, prefetch a Queryset of active postcodes (i.e. the postcodes in which a distributor is active)
"""

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}), required=False)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = MWA_usermodel
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2', )

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and (password1 != password2):
            raise forms.ValidationError("Passwords do not match")
        return(password2)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.username = self.cleaned_data.get('email')
        
        if commit:
            user.save()
        return(user)


class UserLoginForm(forms.Form):
    query = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self,*args,**kwargs):
        query = self.cleaned_data.get('query')
        password = self.cleaned_data.get('password')
        user_qs_final = MWA_usermodel.objects.filter(
                Q(username__iexact=query) |
                Q(email__iexact=query)
        ).distinct()

        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError("Invalid credentials - user does not exist")
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
            raise forms.ValidationError("Invalid credentials")
        self.cleaned_data["user_obj"] = user_obj

        return(super(UserLoginForm,self).clean(*args, **kwargs))
