import warnings
import pandas as pd
import os
import requests
import time
import random
from bs4 import BeautifulSoup
from torrequest import TorRequest
from mywealthanalyst_django.settings import BASE_DIR
from datetime import timedelta

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from MWA_webapp.models import Commodities

from scripts.scrape_livedata_v3 import scrape_current_v3
from scripts.get_historical_data_v2 import update_houseprice, update_annualincome, update_allords_PE_ratio

logger = get_task_logger(__name__)

warnings.filterwarnings("ignore", category=RuntimeWarning)


@periodic_task(
    run_every=(crontab(minute='*/5')),
    name="cron_update_live_prices_v3",
    ignore_result=True
)
def cron_update_live_prices_v3():
    """
    Scrape live prices (to be run every 5 minutes)
    """
    try:
        time.sleep(random.randint(0, 30))
        scrape_current_v3()
    except Exception as exc:
        logger.warning(exc)
        raise Exception


# @periodic_task(
#     run_every=(crontab(hour=0, minute=20, day_of_month="1")),
#     name="cron_update_houseprice_and_annualincome",
#     ignore_result=True
# )
# def cron_update_houseprice_and_annualincome():
#     """
#     Update ABS house price data for 8 capital cities
#     """
#     update_houseprice()
#     update_annualincome()


def helper(commodity_name=None):
    instance = Commodities.objects.get(commodity_name=commodity_name)
    last_price = instance.last_price
    movement = instance.last_movement_nominal
    previous_close = last_price - movement
    return(previous_close)


def updater(filename=None, commodity_name=None, date=None):
    filepath = os.path.join(BASE_DIR, f"../media_files/datasets/{filename}")
    existing = pd.read_csv(filepath)
    if date > pd.to_datetime(existing.iloc[-1, 0], format="%d/%m/%Y").date():
        new = pd.DataFrame(
            data={'Date': [date], 'price_USD': [helper(commodity_name)]})
        new.Date = pd.to_datetime(new.Date, format="%d/%m/%Y")
        existing = pd.concat((existing, new), ignore_index=True)
        existing.to_csv(filepath, index=False, date_format="%d/%m/%Y")


# @periodic_task(
#     run_every=(crontab(hour=0, minute=20)),
#     name="update_historic_from_live_prices",
#     ignore_result=True
# )
# def update_historic_from_live_prices():
#     """
#     Update ABS house price data for 8 capital cities
#     """
#     date = pd.to_datetime('today').date() - pd.Timedelta(1, unit='d')
#     updater('allords.csv', 'All Ords', date)
#     updater('bitcoin.csv', 'Bitcoin', date)
#     updater('gold.csv', 'Gold', date)
#     updater('silver.csv', 'Silver', date)
#     updater('aud.csv', 'AUD', date)
#     update_allords_PE_ratio()
