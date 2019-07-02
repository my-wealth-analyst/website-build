import pandas as pd
import numpy as np
import os
import requests

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core import mail
from django.utils.html import strip_tags

from mywealthanalyst_django.settings import BASE_DIR
from .models import MWA_usermodel
from .forms import UserLoginForm, RegistrationForm
from .tokens import account_activation_token


# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)
        if form.is_valid():

            user = form.save(commit=False)
            user.activated = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your mywealthanalyst account.'
            html_message = render_to_string('MWA_users/confirmation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),#.decode(),
                'token': account_activation_token.make_token(user),
            })
            plain_message = strip_tags(html_message)
            from_email = 'mywealthanalyst <register@mywealthanalyst.com>'
            to_email = [form.cleaned_data.get('email')]

            mail.send_mail(mail_subject, plain_message, from_email, to_email, html_message=html_message)

            return(render(request, "MWA_users/please_confirm_email.html"))
    else:
        form = RegistrationForm()

    return(render(request, "MWA_users/register.html", {'form': form}))


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MWA_usermodel.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MWA_usermodel.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.activated = True
        user.save()
        login(request, user)
        return(render(request, "MWA_users/email_confirmed.html"))
    else:
        return(render(request, "MWA_users/email_invalid.html"))


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            user_obj = form.cleaned_data.get('user_obj')
            login(request, user_obj)
            return(HttpResponseRedirect(reverse('dashboard')))
    else:
        form = UserLoginForm()

    return(render(request, "MWA_users/login.html", {'form': form}))


def logout_view(request):
    logout(request)
    return(HttpResponseRedirect(reverse('login')))
