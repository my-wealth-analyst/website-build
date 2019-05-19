import pandas as pd
from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
# Create your models here.

my_validator = RegexValidator(r'^\+?1?\d{9,15}$', "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class MWA_usermodel(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True) # changes email to unique and blank to false
    REQUIRED_FIELDS = [] # removes email from REQUIRED_FIELDS

    phone_number = models.CharField(null=True, blank=True, validators=[my_validator], max_length=15)
    country = models.CharField(null=True, blank=True, max_length=20)

    def __str__(self):
        return "%s" % (self.username)
