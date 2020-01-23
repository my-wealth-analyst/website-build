import time
import datetime
import requests
import os
import io
from functools import reduce
import random

from mywealthanalyst_django.settings import BASE_DIR

import pandas as pd
import numpy as np

from MWA_webapp.models import Commodities, Commodity_TS


def populate_gold():
    df = pd.read_csv("../media_files/datasets/gold.csv")
    df.Date = pd.to_datetime(df.Date, format="%d/%m/%Y")
    df = df.fillna(method='pad', axis=0)

    for index, row in df.iterrows():
        date = row['Date']
        date = date  # .date
        price = row['price_USD']

        record, created = Commodity_TS.objects.get_or_create(
            name__iexact='Gold', date=date)
        record.last_price = price
        record.save()


def populate_silver():
    df = pd.read_csv("../media_files/datasets/silver.csv")
    df.Date = pd.to_datetime(df.Date, format="%d/%m/%Y")
    df = df.fillna(method='pad', axis=0)

    for index, row in df.iterrows():
        date = row['Date']
        date = date  # .date
        price = row['price_USD']

        record, created = Commodity_TS.objects.get_or_create(
            name__iexact='Silver', date=date)
        record.last_price = price
        record.save()


def populate_aud():
    df = pd.read_csv("../media_files/datasets/aud.csv")
    df.Date = pd.to_datetime(df.Date, format="%d/%m/%Y")
    df = df.fillna(method='pad', axis=0)

    for index, row in df.iterrows():
        date = row['Date']
        date = date  # .date
        price = row['price_USD']

        record, created = Commodity_TS.objects.get_or_create(
            name__iexact='AUD', date=date)
        record.last_price = price
        record.save()


def populate_allords_pe_ratio():
    df = pd.read_csv("../media_files/datasets/allordsperatio.csv")
    df.Date = pd.to_datetime(df.Date, format="%d/%m/%Y")
    df = df.fillna(method='pad', axis=0)

    for index, row in df.iterrows():
        date = row['Date']
        date = date  # .date
        price = row['price_USD']

        record, created = Commodity_TS.objects.get_or_create(
            name__iexact='Allordsperatio', date=date)
        record.last_price = price
        record.save()


def populate_allords():
    df = pd.read_csv("../media_files/datasets/allords.csv")
    df.Date = pd.to_datetime(df.Date, format="%d/%m/%Y")
    df = df.fillna(method='pad', axis=0)

    for index, row in df.iterrows():
        date = row['Date']
        date = date  # .date
        price = row['price_USD']

        record, created = Commodity_TS.objects.get_or_create(
            name__iexact='Allords', date=date)
        record.last_price = price
        record.save()


def populate_bitcoin():
    df = pd.read_csv("../media_files/datasets/bitcoin.csv")
    df.Date = pd.to_datetime(df.Date, format="%d/%m/%Y")
    df = df.fillna(method='pad', axis=0)

    for index, row in df.iterrows():
        date = row['Date']
        date = date  # .date
        price = row['price_USD']

        record, created = Commodity_TS.objects.get_or_create(
            name__iexact='Bitcoin', date=date)
        record.last_price = price
        record.save()
