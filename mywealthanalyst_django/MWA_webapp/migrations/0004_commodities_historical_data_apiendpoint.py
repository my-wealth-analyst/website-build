# Generated by Django 2.2.2 on 2019-07-09 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MWA_webapp', '0003_commodities_historical_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='commodities',
            name='historical_data_APIendpoint',
            field=models.CharField(blank=True, help_text='DO NOT CHANGE', max_length=20, null=True),
        ),
    ]
