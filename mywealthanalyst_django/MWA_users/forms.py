import os
from django import forms
from django.conf import settings

from django.db import models
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm

from .models import MWA_usermodel


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = MWA_usermodel
        fields = ('email',
                  # 'first_name', 'last_name', 'phone_number',
                  'password1', 'password2', )

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username
        try:
            match = MWA_usermodel.objects.get(email=email)
        except MWA_usermodel.DoesNotExist:
            # Unable to find a user, this is fine
            return(email)
        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('this email address is already in use')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("passwords do not match")
        return(password2)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.username = self.cleaned_data.get('email')

        if commit:
            user.save()
        return(user)


class UserLoginForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


    def clean(self,*args,**kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        try:
            match = MWA_usermodel.objects.get(email=email)
            # return(email)
        except MWA_usermodel.DoesNotExist:
            # Unable to find a user
            raise forms.ValidationError("Email does not exist")

        user_obj = match
        if not user_obj.check_password(password):
            raise forms.ValidationError("Invalid credentials")
        self.cleaned_data["user_obj"] = user_obj

        return(super(UserLoginForm,self).clean(*args, **kwargs))
