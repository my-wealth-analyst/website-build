from django.contrib import admin
from .models import (
                    Commodities
                    )
from scripts.perthmint_getdata import data_update_commodity, delete_commodity_file
from scripts.scrape_livedata import scrape_all

def refresh_data(ModelAdmin, request, queryset):
    scrape_all()

class CommoditiesAdmin(admin.ModelAdmin):
    actions = [refresh_data]
    readonly_fields = ["date_last_scraped"]
    list_display = ['commodity_name','enabled','date_last_scraped','last_price']






# Register your models here.

admin.site.register(Commodities, CommoditiesAdmin)
