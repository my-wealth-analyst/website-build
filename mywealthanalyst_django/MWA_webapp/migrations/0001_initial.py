# Generated by Django 2.2.1 on 2019-05-30 10:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commodities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField()),
                ('commodity_name', models.CharField(max_length=20)),
                ('date_last_scraped', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('last_price', models.FloatField(blank=True, help_text='Value in USD, or index value', null=True)),
                ('last_movement_nominal', models.FloatField(blank=True, help_text='Value in USD, or index value', null=True)),
                ('last_movement_percentage', models.FloatField(blank=True, help_text='Value in percent ("5" = 5%)', null=True)),
            ],
        ),
    ]
