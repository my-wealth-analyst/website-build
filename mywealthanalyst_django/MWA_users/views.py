import pandas as pd
import numpy as np
import os
import requests

from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import login, get_user_model, logout

from mywealthanalyst_django.settings import BASE_DIR
from .models import MWA_usermodel
from .forms import UserLoginForm, RegistrationForm


# Create your views here.


def register_view(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return(HttpResponseRedirect(reverse('dashboard')))

    return( render(request, "MWA_users/register.html", {'form':form}))

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user_obj = form.cleaned_data.get('user_obj')
        login(request, user_obj)
        return(HttpResponseRedirect(reverse('dashboard')))
    return( render(request, "MWA_users/login.html", {'form':form}))

def logout_view(request):
    logout(request)
    return(HttpResponseRedirect(reverse('login')))
