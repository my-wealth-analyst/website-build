import time, datetime
import requests
import os, io

from mywealthanalyst_django.settings import BASE_DIR

import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup



def goldsilver_scraperfunction(commodity = None):
    """
    Scrapes Perthmint website for historical silver and gold prices.
    Perth mint stores these as CSV files, in same format for silver and gold.
    This function is generalised for 'commodity' and is called below for each of 'gold' and 'silver'
    """

    filepath = os.path.join(BASE_DIR,f"../media_files/datasets/{commodity}_askprice_avg_aud.csv")

    if os.path.isfile(filepath):
        old_data = pd.read_csv(filepath, parse_dates=True)
        old_data.Date = pd.to_datetime(old_data.Date)
        old_data.set_index('Date',inplace=True)

        url = f'http://www.perthmint.com.au/treasury/{commodity}-Current.csv'
        df = pd.read_csv(url,header=0)
        df = df[['Market','Perth Mint Spot.15']]
        df.columns = ['Date','AskPrice_Avg_AUD']
        df.dropna(axis=0,how='any',inplace=True)
        df = df.iloc[4:,:]
        df.Date = pd.to_datetime(df.Date , format = '%d/%m/%y')
        df.set_index('Date',inplace=True)
        df = df[~df.index.duplicated()]

        df.AskPrice_Avg_AUD = df.AskPrice_Avg_AUD.astype(str)
        df.AskPrice_Avg_AUD = df.AskPrice_Avg_AUD.str.strip()
        df.AskPrice_Avg_AUD = df.AskPrice_Avg_AUD.str.replace(',', '')
        df.AskPrice_Avg_AUD = df.AskPrice_Avg_AUD.astype('float')

        new_data = pd.concat((old_data,df),axis=0,join='outer')
        new_data = new_data[~new_data.index.duplicated()]

        new_data.reset_index(inplace=True)
        new_data.to_csv(filepath, index=False)

    else:
        url = f'http://www.perthmint.com.au/treasury/{commodity}.csv'
        df = pd.read_csv(url,header=0)
        df = df[['Market','Perth Mint Spot.15']]
        df.columns = ['Date','AskPrice_Avg_AUD']
        df.dropna(axis=0,how='any',inplace=True)
        df = df.iloc[4:,:]
        df.Date = pd.to_datetime(df.Date , format = '%d/%m/%y')
        df.set_index('Date',inplace=True)

        df.AskPrice_Avg_AUD = df.AskPrice_Avg_AUD.astype(str)
        df.AskPrice_Avg_AUD = df.AskPrice_Avg_AUD.str.strip()
        df.AskPrice_Avg_AUD = df.AskPrice_Avg_AUD.str.replace(',', '')
        df.AskPrice_Avg_AUD = df.AskPrice_Avg_AUD.astype('float')

        df = df[~df.index.duplicated()]
        df.reset_index(inplace=True)

        df.to_csv(filepath, index=False)

def update_gold_and_silver():
    goldsilver_scraperfunction('gold')
    goldsilver_scraperfunction('silver')
    goldsilver_scraperfunction('gold')
    goldsilver_scraperfunction('silver')

def update_oil():
    """
    Scrapes Markinsider website for historical WTI crude oil prices (in usd).
    Data is presented as a single full html table
    """
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.headless = True

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument('user-agent={0}'.format(user_agent))

    driver = webdriver.Chrome(chrome_options=options)
    driver.set_page_load_timeout(10)

    filepath = os.path.join(BASE_DIR,f"../media_files/datasets/oil_askprice_avg_aud.csv")
    date = datetime.date.today().strftime('%d.%m.%Y')

    try:
        page = driver.get(f'https://markets.businessinsider.com/commodities/historical-prices/oil-price/usd/1.1.2005_{date}?type=wti')
        time.sleep(5)
    except TimeoutException:
        pass
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    table = soup.find('table', {'class':'table instruments'})
    df = pd.read_html(str(table))[0]

    df = df[['Date','Open']]
    df.columns = ['Date','AskPrice_Avg_AUD']
    df.to_csv(filepath, index=False)
    driver.close()

def update_bitcoin():
    """
    Scrapes Coinmarketcap website for historical bitcoin prices (in usd).
    Data is presented as a single full html table
    """
    filepath = os.path.join(BASE_DIR,f"../media_files/datasets/bitcoin_askprice_avg_aud.csv")
    date = datetime.date.today().strftime('%Y%m%d')

    url = f'https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end={date}'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    df = pd.read_html(str(soup.find('div',{'class':"table-responsive"}).find('table',{'class':'table'})))[0]
    df = df[['Date','Open*']]
    df.columns = ['Date','AskPrice_Avg_AUD']
    df.to_csv(filepath, index=False)

def update_allords_PE_ratio():

    filepath = os.path.join(BASE_DIR,f"../media_files/datasets/allordsperatio_askprice_avg_aud.csv")

    url = 'https://www.marketindex.com.au/sites/default/files/statistics/asx-fundamentals.xlsx'
    r = requests.get(url)

    with open(os.path.join(BASE_DIR,f"../media_files/datasets/asx-fundamentals.xlsx"), 'wb') as f:
        f.write(r.content)

    df = pd.read_excel(os.path.join(BASE_DIR,f"../media_files/datasets/asx-fundamentals.xlsx"), header=9)

    df = df[['Date','PE Ratio']]
    df.columns = ['Date','AskPrice_Avg_AUD']
    df.dropna(axis=0,how='any',inplace=True)

    df.to_csv(filepath, index=False)

def update_allords():
    """
    Scrapes Markinsider website for historical WTI crude oil prices (in usd).
    Data is presented as a single full html table
    """
    filepath = os.path.join(BASE_DIR,f"../media_files/datasets/allords_askprice_avg_aud.csv")
    date = int(time.time())

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.headless = True

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument('user-agent={0}'.format(user_agent))

    driver = webdriver.Chrome(chrome_options=options)
    driver.set_page_load_timeout(10)

    try:
        page = driver.get(f'https://au.finance.yahoo.com/quote/%5EAORD/history?period1=460303200&period2={date}&interval=1d&filter=history&frequency=1d')
    except TimeoutException:
        pass

    url = driver.find_element_by_xpath('//a[@download="^AORD.csv"]').get_attribute("href")

    driver_cookies = driver.get_cookies()
    c = {c['name']:c['value'] for c in driver_cookies}
    res = requests.get(url,cookies=c).content
    df = pd.read_csv(io.StringIO(res.decode('utf-8')))

    df = df[['Date','Open']]
    df.columns = ['Date','AskPrice_Avg_AUD']
    df.to_csv(filepath, index=False)

    driver.close()
