import pandas as pd

from django.db import models

# Create your models here.

class Commodities(models.Model):
    enabled = models.BooleanField()
    commodity_name = models.CharField(max_length = 20)

    def __str__(self):
        return "%s" % (self.commodity_name)
