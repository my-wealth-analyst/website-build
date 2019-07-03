from django.contrib import admin
from .models import (
                    Commodities
                    )
from scripts.get_historical_data import update_gold_and_silver, update_oil, update_bitcoin, update_allords_PE_ratio, update_allords
from scripts.scrape_livedata_v2 import scrape_current_v2


def create_commodities():
    Commodities.objects.get_or_create(commodity_name="All Ords", enabled=True)
    Commodities.objects.get_or_create(commodity_name="Gold", enabled=True)
    Commodities.objects.get_or_create(commodity_name="Silver", enabled=True)
    Commodities.objects.get_or_create(commodity_name="Oil", enabled=True)
    Commodities.objects.get_or_create(commodity_name="Bitcoin", enabled=True)
    Commodities.objects.get_or_create(commodity_name="Property", enabled=True)
    Commodities.objects.get_or_create(commodity_name="AUD", enabled=False)

def refresh_historical_data(ModelAdmin, request, queryset):
    create_commodities()
    update_gold_and_silver()
    update_oil()
    update_bitcoin()
    update_allords_PE_ratio()
    update_allords()

def scrape_live_data(ModelAdmin, request, queryset):
    scrape_current_v2()

class CommoditiesAdmin(admin.ModelAdmin):
    actions = [refresh_historical_data, scrape_live_data]
    readonly_fields = ["date_last_scraped"]
    list_display = ['commodity_name','enabled','date_last_scraped','last_price']

# Register your models here.

admin.site.register(Commodities, CommoditiesAdmin)
