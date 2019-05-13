from django.contrib import admin
from .models import (
                    Commodities
                    )
from scripts.perthmint_getdata import data_update_commodity, delete_commodity_file

def refresh_data(ModelAdmin, request, queryset):

    delete_commodity_file('gold')
    delete_commodity_file('silver')
    data_update_commodity('gold')
    data_update_commodity('gold')
    data_update_commodity('silver')
    data_update_commodity('silver')

class CommoditiesAdmin(admin.ModelAdmin):
    actions = [refresh_data]
    list_display = ['commodity_name','enabled']


# Register your models here.

admin.site.register(Commodities, CommoditiesAdmin)
