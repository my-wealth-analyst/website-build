import pandas as pd
from datetime import date

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
# Create your models here.

my_validator = RegexValidator(r'^\+?1?\d{9,15}$', "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class MWA_usermodelManager(BaseUserManager):
    def create_user(self, password, email):
        """
        Creates and saves a User with the given username, password, email,
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username = email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, email, **kwargs):
        user = self.create_user(password, email, **kwargs)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MWA_usermodel(AbstractUser):
    objects = MWA_usermodelManager()
    USERNAME_FIELD = 'email'

    email = models.EmailField(_('email address'), unique=True) # changes email to unique and blank to false
    REQUIRED_FIELDS = []  # removes email from REQUIRED_FIELDS

    phone_number = models.CharField(null=True, blank=True,
                                    validators=[my_validator], max_length=15)
    country = models.CharField(null=True, blank=True, max_length=20)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return "%s" % (self.email)
