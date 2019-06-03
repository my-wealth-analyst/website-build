from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
import requests
from bs4 import BeautifulSoup
import re
from MWA_webapp.models import Commodities
from datetime import datetime


def scrape_ALLORDS(driver):
    """ ALL ORDINARIES"""
    try:
        page = driver.get('https://www.marketindex.com.au/all-ordinaries')
    except TimeoutException:
        pass
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    allords_last_price = float(soup.find("p",{'class':'quoteapi-number'}).text.strip().replace(",",""))
    allords_last_movement_nominal = float(soup.find("span",{'class':'quoteapi-change'}).text.strip().replace(",",""))
    allords_last_movement_percentage = float(soup.find("span",{'class':'quoteapi-pct-change'}).text.strip().replace(",","").replace("%","").replace("(","").replace(")",""))

    ALLORDS = [allords_last_price,allords_last_movement_nominal,allords_last_movement_percentage]
    return(ALLORDS)


def scrape_OIL(driver):
    """ CRUDE OIL (WTI)"""
    try:
        page = driver.get('https://www.marketindex.com.au/crude-oil')
    except TimeoutException:
        pass
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    WTIoil_last_price = float(re.sub("[^0-9.]", "", soup.find("div",{'class':'price-wrapper'}).find("p").text))
    if soup.find("div",{'class':'movement-wrapper'}).find('div',{'class':'negative'}) is None:
        WTIoil_last_movement_nominal = float(re.sub("[^0-9.]", "", soup.find("div",{'class':'movement-wrapper'}).text.split("(")[0]))
        WTIoil_last_movement_percentage = float(re.sub("[^0-9.]", "", soup.find("div",{'class':'movement-wrapper'}).text.split("(")[1]))
    else:
        WTIoil_last_movement_nominal = -1*abs(float(re.sub("[^0-9.]", "", soup.find("div",{'class':'movement-wrapper'}).text.split("(")[0])))
        WTIoil_last_movement_percentage = -1*abs(float(re.sub("[^0-9.]", "", soup.find("div",{'class':'movement-wrapper'}).text.split("(")[1])))

    WTIOIL = [WTIoil_last_price,WTIoil_last_movement_nominal,WTIoil_last_movement_percentage]
    return(WTIOIL)


def scrape_GOLD(driver):
    """ GOLD """
    try:
        page = driver.get('https://www.marketindex.com.au/gold')
    except TimeoutException:
        pass
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    gold_last_price = float(re.sub("[^0-9.]", "", soup.find("div",{'class':'price-wrapper'}).find("p").text))
    if soup.find("div",{'class':'movement-wrapper'}).find('div',{'class':'negative'}) is None:
        gold_last_movement_nominal = float(re.sub("[^0-9.]", "", soup.find("div",{'class':'movement-wrapper'}).text.split("(")[0]))
        gold_last_movement_percentage = float(re.sub("[^0-9.]", "", soup.find("div",{'class':'movement-wrapper'}).text.split("(")[1]))
    else:
        gold_last_movement_nominal = -1*abs(float(re.sub("[^0-9.]", "", soup.find("div",{'class':'movement-wrapper'}).text.split("(")[0])))
        gold_last_movement_percentage = -1*abs(float(re.sub("[^0-9.]", "", soup.find("div",{'class':'movement-wrapper'}).text.split("(")[1])))

    GOLD = [gold_last_price,gold_last_movement_nominal,gold_last_movement_percentage]
    return(GOLD)

def scrape_SILVER(driver):
    """ SILVER """
    try:
        page = driver.get('https://www.marketindex.com.au/silver')
    except TimeoutException:
        pass
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    silver_last_price = float(re.sub("[^0-9.]", "", soup.find("div",{'class':'price-wrapper'}).find("p").text))
    if soup.find("div",{'class':'movement-wrapper'}).find('div',{'class':'negative'}) is None:
        silver_last_movement_nominal = float(re.sub("[^0-9.]", "", soup.find("div",{'class':'movement-wrapper'}).text.split("(")[0]))
        silver_last_movement_percentage = float(re.sub("[^0-9.]", "", soup.find("div",{'class':'movement-wrapper'}).text.split("(")[1]))
    else:
        silver_last_movement_nominal = -1*abs(float(re.sub("[^0-9.]", "", soup.find("div",{'class':'movement-wrapper'}).text.split("(")[0])))
        silver_last_movement_percentage = -1*abs(float(re.sub("[^0-9.]", "", soup.find("div",{'class':'movement-wrapper'}).text.split("(")[1])))

    SILVER = [silver_last_price,silver_last_movement_nominal,silver_last_movement_percentage]
    return(SILVER)

def scrape_BITCOIN(driver):
    """ BITCOIN """
    try:
        page = driver.get('https://coinmarketcap.com/currencies/bitcoin/')
    except TimeoutException:
        pass
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    bitcoin_last_price = float(re.sub("[^0-9.]", "", soup.find("span",{'class':'details-panel-item--price__value'}).text))

    if soup.find('span',{'class':'negative_change'}) is None:
        bitcoin_last_movement_percentage = abs(float(re.sub("[^0-9.]", "", soup.find("span",{'data-format-percentage':True})['data-format-value'])))
    else:
        bitcoin_last_movement_percentage = -1*abs(float(re.sub("[^0-9.]", "", soup.find("span",{'data-format-percentage':True})['data-format-value'])))

    silver_last_movement_nominal = bitcoin_last_price*bitcoin_last_movement_percentage/100

    BITCOIN = [bitcoin_last_price,silver_last_movement_nominal,bitcoin_last_movement_percentage]
    return(BITCOIN)




def scrape_all():

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.headless = True

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument('user-agent={0}'.format(user_agent))


    driver = webdriver.Chrome(chrome_options=options)
    driver.set_page_load_timeout(15)

    try:
        r = requests.get('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=AUD&to_currency=USD&apikey=M4TA2P8B2OU22SPC')
        json_response = r.json()

        Commodities.objects.filter(commodity_name="AUD").update(date_last_scraped=datetime.now(), last_price=json_response["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    except Exception as e:
        print('error scraping AUD: ', e)

    try:
        update = scrape_ALLORDS(driver)
        exch_rate = Commodities.objects.get(commodity_name="AUD").last_price
        update[0] = update[0]*exch_rate
        update[1] = update[1]*exch_rate

        Commodities.objects.filter(commodity_name="All Ords").update(date_last_scraped=datetime.now(), last_price=update[0], last_movement_nominal=update[1], last_movement_percentage=update[2])
    except Exception as e:
        print('error scraping ALLORDS: ', e)

    try:
        update = scrape_OIL(driver)
        Commodities.objects.filter(commodity_name="Oil").update(date_last_scraped=datetime.now(), last_price=update[0], last_movement_nominal=update[1], last_movement_percentage=update[2])
    except Exception as e:
        print('error scraping OIL: ', e)

    try:
        update = scrape_BITCOIN(driver)
        Commodities.objects.filter(commodity_name="Bitcoin").update(date_last_scraped=datetime.now(), last_price=update[0], last_movement_nominal=update[1], last_movement_percentage=update[2])
    except Exception as e:
        print('error scraping BITCOIN: ', e)

    try:
        update = scrape_GOLD(driver)
        Commodities.objects.filter(commodity_name="Gold").update(date_last_scraped=datetime.now(), last_price=update[0], last_movement_nominal=update[1], last_movement_percentage=update[2])
    except Exception as e:
        print('error scraping GOLD: ', e)

    try:
        update = scrape_SILVER(driver)
        Commodities.objects.filter(commodity_name="Silver").update(date_last_scraped=datetime.now(), last_price=update[0], last_movement_nominal=update[1], last_movement_percentage=update[2])
    except Exception as e:
        print('error scraping SILVER: ', e)


    driver.close()
