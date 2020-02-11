from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from .models import (
    Commodities,
    Commodity_TS
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
    readonly_fields = ["date_last_scraped", "historical_data_APIendpoint"]
    list_display = ['commodity_name', 'enabled',
                    'date_last_scraped', 'last_price']


class CommoditiesTSAdmin(admin.ModelAdmin):
    list_filter = (('date', DateFieldListFilter), 'name')
    list_display = ['date', 'name', 'last_price']
    fields = ['name', 'date', 'datetime', 'last_price',
              'last_movement_nominal', 'last_movement_percentage']
    readonly_fields = ('datetime',)

# Register your models here.


admin.site.register(Commodities, CommoditiesAdmin)
admin.site.register(Commodity_TS, CommoditiesTSAdmin)
