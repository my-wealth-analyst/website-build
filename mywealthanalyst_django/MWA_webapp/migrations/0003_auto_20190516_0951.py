# Generated by Django 2.2.1 on 2019-05-15 23:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MWA_webapp', '0002_auto_20190513_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='commodities',
            name='date_last_scraped',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='commodities',
            name='last_movement_nominal',
            field=models.FloatField(blank=True, help_text='Value in USD, or index value', null=True),
        ),
        migrations.AddField(
            model_name='commodities',
            name='last_movement_percentage',
            field=models.FloatField(blank=True, help_text='Value in percent ("5" = 5%)', null=True),
        ),
        migrations.AddField(
            model_name='commodities',
            name='last_price',
            field=models.FloatField(blank=True, help_text='Value in USD, or index value', null=True),
        ),
    ]
