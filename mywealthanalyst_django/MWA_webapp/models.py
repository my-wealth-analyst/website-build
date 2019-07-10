import os
import pandas as pd
from datetime import date
from django.db import models
from django.utils import timezone

from django.conf import settings
from django.core.files.storage import FileSystemStorage

class MyFileStorage(FileSystemStorage):

    # This method is actually defined in Storage
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name # simply returns the name passed

class Commodities(models.Model):
    enabled = models.BooleanField()
    commodity_name = models.CharField(max_length = 20)
    display_order = models.IntegerField(default=1, null=True)
    date_last_scraped = models.DateTimeField(null=True,blank=True, default= timezone.now )
    last_price = models.FloatField(null=True,blank=True, help_text='Value in USD, or index value')
    last_movement_nominal = models.FloatField(null=True,blank=True, help_text='Value in USD, or index value')
    last_movement_percentage = models.FloatField(null=True,blank=True, help_text='Value in percent ("5" = 5%)')
    historical_data = models.FileField(upload_to='datasets/', storage=MyFileStorage(), null=True,blank=True, help_text="historical data in csv format (don't change column names or format)")
    historical_data_APIendpoint = models.CharField(max_length=20, null=True,blank=True)

    def __str__(self):
        return "%s" % (self.commodity_name)

    def save(self, *args, **kwargs):
        if self.historical_data.name:
            self.historical_data.name = self.historical_data_APIendpoint
        super(Commodities, self).save(*args, **kwargs)
