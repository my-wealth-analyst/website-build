from django.contrib import admin
from .models import (
                    Commodities
                    )
from scripts.get_historical_data import update_gold_and_silver, update_oil, update_bitcoin, update_allords_PE_ratio
from scripts.scrape_livedata import scrape_all

def refresh_data(ModelAdmin, request, queryset):
    update_gold_and_silver()
    update_oil()
    update_bitcoin()
    update_allords_PE_ratio()


class CommoditiesAdmin(admin.ModelAdmin):
    actions = [refresh_data]
    readonly_fields = ["date_last_scraped"]
    list_display = ['commodity_name','enabled','date_last_scraped','last_price']

# Register your models here.

admin.site.register(Commodities, CommoditiesAdmin)
