import pandas as pd
import numpy as np
import os
import requests

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from mywealthanalyst_django.settings import BASE_DIR


# from .models import Commodities


# Create your views here.

def login(request):

    return HttpResponse('Login page')


def register(request):

    return HttpResponse('Register page')
