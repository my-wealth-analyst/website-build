from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import (
                    MWA_usermodel
                    )

class MWA_usermodel_Admin(admin.ModelAdmin):
    list_display = ['email' , 'last_name' , 'first_name' , 'last_login' , 'phone_number' , 'country' ]

    fieldsets = (
        (None, {'fields': ('email', 'activated', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'country')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'activated')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


# Register your models here.

admin.site.register(MWA_usermodel, MWA_usermodel_Admin)
