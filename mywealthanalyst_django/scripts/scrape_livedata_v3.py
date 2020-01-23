from bs4 import BeautifulSoup
from torrequest import TorRequest
from MWA_webapp.models import Commodities, Commodity_TS
from datetime import datetime
import random
from django.conf import settings
from celery.utils.log import get_task_logger
import requests

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


logger = get_task_logger(__name__)


def helper(soup=None, title=None):
    base_element = soup.find("a", {'title': title})
    price = base_element.findNext('td')
    price_change = price.findNext('td')
    price_change_perc = price_change.findNext('td')

    price = float(price.text.replace(",", ""))
    price_change = float(price_change.text.replace(",", ""))
    price_change_perc = float(price_change_perc.text.replace("%", ""))

    return({'price': price, 'price_change': price_change, 'price_change_perc': price_change_perc})


user_agent_list = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


def scrape_current_v3():

    tr = TorRequest(password='mywealthanalyst_admin')
    tr.reset_identity()  # Reset Tor
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent, }

    current_ip = tr.get('http://ipecho.net/plain').text

    response = tr.get('https://au.investing.com/', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    AUD = helper(soup=soup, title='AUD/USD - Australian Dollar US Dollar')

    OIL_USD = helper(soup=soup, title='Crude Oil WTI Futures (CFD)')
    GOLD_USD = helper(soup=soup, title='Gold Futures (CFD)')
    SILVER_USD = helper(soup=soup, title='Silver Futures (CFD)')
    BITCOIN_USD = helper(soup=soup, title='BTC/USD - Bitcoin US Dollar')

    ALLORDS_AUD = helper(soup=soup, title='ASX All Ordinaries')
    ALLORDS_USD = ALLORDS_AUD
    ALLORDS_USD["price"] = ALLORDS_USD["price"]*AUD["price"]
    ALLORDS_USD["price_change"] = ALLORDS_USD["price_change"]*AUD["price"]

    record, created = Commodity_TS.objects.get_or_create(
        name='AUD', date=datetime.now())
    record.last_price = AUD["price"]
    record.last_movement_nominal = AUD["price_change"]
    record.last_movement_percentage = AUD["price_change_perc"]
    record.save()

    record, created = Commodity_TS.objects.get_or_create(
        name='Oil', date=datetime.now())
    record.last_price = OIL_USD["price"]
    record.last_movement_nominal = OIL_USD["price_change"]
    record.last_movement_percentage = OIL_USD["price_change_perc"]
    record.save()

    record, created = Commodity_TS.objects.get_or_create(
        name='Gold', date=datetime.now())
    record.last_price = GOLD_USD["price"]
    record.last_movement_nominal = GOLD_USD["price_change"]
    record.last_movement_percentage = GOLD_USD["price_change_perc"]
    record.save()

    record, created = Commodity_TS.objects.get_or_create(
        name='Silver', date=datetime.now())
    record.last_price = SILVER_USD["price"]
    record.last_movement_nominal = SILVER_USD["price_change"]
    record.last_movement_percentage = SILVER_USD["price_change_perc"]
    record.save()

    record, created = Commodity_TS.objects.get_or_create(
        name='Bitcoin', date=datetime.now())
    record.last_price = BITCOIN_USD["price"]
    record.last_movement_nominal = BITCOIN_USD["price_change"]
    record.last_movement_percentage = BITCOIN_USD["price_change_perc"]
    record.save()

    record, created = Commodity_TS.objects.get_or_create(
        name='Allords', date=datetime.now())
    record.last_price = ALLORDS_USD["price"]
    record.last_movement_nominal = ALLORDS_USD["price_change"]
    record.last_movement_percentage = ALLORDS_USD["price_change_perc"]
    record.save()

    logger.info(f"Live prices updated using IP: {current_ip}")
