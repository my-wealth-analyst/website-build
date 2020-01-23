# Generated by Django 2.2.2 on 2020-01-22 21:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MWA_webapp', '0005_auto_20190710_1854'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commodity_TS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('commodity_name', models.CharField(max_length=20)),
                ('last_price', models.FloatField(blank=True, help_text='Value in USD, or index value', null=True)),
                ('last_movement_nominal', models.FloatField(blank=True, help_text='Value in USD, or index value', null=True)),
                ('last_movement_percentage', models.FloatField(blank=True, help_text='Value in percent ("5" = 5%)', null=True)),
            ],
        ),
    ]
