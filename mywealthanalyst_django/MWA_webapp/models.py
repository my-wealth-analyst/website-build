import pandas as pd
from datetime import date
from django.db import models
from django.utils import timezone

# Create your models here.

class Commodities(models.Model):
    enabled = models.BooleanField()
    commodity_name = models.CharField(max_length = 20)
    display_order = models.IntegerField(default=1, null=True)
    date_last_scraped = models.DateTimeField(null=True,blank=True, default= timezone.now )
    last_price = models.FloatField(null=True,blank=True, help_text='Value in USD, or index value')
    last_movement_nominal = models.FloatField(null=True,blank=True, help_text='Value in USD, or index value')
    last_movement_percentage = models.FloatField(null=True,blank=True, help_text='Value in percent ("5" = 5%)')

    def __str__(self):
        return "%s" % (self.commodity_name)
