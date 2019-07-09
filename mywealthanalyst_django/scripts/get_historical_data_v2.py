import time, datetime
import requests
import os, io
from functools import reduce

from mywealthanalyst_django.settings import BASE_DIR

import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from torrequest import TorRequest

user_agent_list = [
   #Chrome
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
    #Firefox
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


def build_datasets():
    gold = quandl.get("LBMA/GOLD")
    gold = gold[["USD (AM)"]]
    gold.columns = ['price_USD']
    gold.to_csv(os.path.join(BASE_DIR,f"../media_files/datasets/gold_usd.csv"))

    silver = quandl.get("LBMA/SILVER")
    silver = silver[["USD"]]
    silver.columns = ['price_USD']
    silver.to_csv(os.path.join(BASE_DIR,f"../media_files/datasets/silver_usd.csv"))


def update_houseprice():
    url = "https://www.abs.gov.au/ausstats/meisubs.nsf/log?openagent&641604.xls&6416.0&Time%20Series%20Spreadsheet&55CB84AAC829D752CA25841C0017D0EF&0&Mar%202019&18.06.2019&Latest"
    df = pd.read_excel(url, sheet_name="Data1", header=0)
    df = df.rename(columns = {'Unnamed: 0':'Date'})
    df = df.set_index('Date')
    df = df.iloc[9:,:]
    df = df[['Median Price of Established House Transfers (Unstratified) ;  Sydney ;',
             'Median Price of Established House Transfers (Unstratified) ;  Melbourne ;',
             'Median Price of Established House Transfers (Unstratified) ;  Brisbane ;',
             'Median Price of Established House Transfers (Unstratified) ;  Adelaide ;',
             'Median Price of Established House Transfers (Unstratified) ;  Perth ;',
             'Median Price of Established House Transfers (Unstratified) ;  Canberra ;',
             'Median Price of Established House Transfers (Unstratified) ;  Hobart ;',
             'Median Price of Established House Transfers (Unstratified) ;  Darwin ;'
           ]]
    df.columns = ['SYD', 'MEL', 'BRI', 'ADE', 'PER', 'CAN', 'HOB', 'DAR']
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d")

    existing = pd.read_csv(os.path.join(BASE_DIR,f"../media_files/datasets/houseprice.csv"), index_col=0)
    existing.index = pd.to_datetime(existing.index, format="%Y-%m-%d")

    new = pd.concat((existing, df[df.index > existing.index[-1]]))
    new.to_csv(os.path.join(BASE_DIR,f"../media_files/datasets/houseprice.csv"))

def helper(state, url):
    df = pd.read_excel(url, sheet_name="Data1", header=0)
    df = df.rename(columns={'Unnamed: 0': 'Date'})
    df = df.iloc[9:,:]
    df.Date = pd.to_datetime(df.Date, format="%b-%Y")
    df['Date'] = df['Date'].apply(lambda dt: dt.replace(day=1))
    df = df.set_index('Date')
    df = df.iloc[:,8]
    df.name = state
    return(df)

def update_annualincome():

    SYD = helper('SYD', "https://www.abs.gov.au/ausstats/meisubs.nsf/log?openagent&63020013a.xls&6302.0&Time%20Series%20Spreadsheet&6F24E359166803C9CA2583A700120BD2&0&Nov%202018&21.02.2019&Latest")
    MEL = helper('MEL', "https://www.abs.gov.au/ausstats/meisubs.nsf/log?openagent&63020013b.xls&6302.0&Time%20Series%20Spreadsheet&B6E021BB24B453C3CA2583A700120C3B&0&Nov%202018&21.02.2019&Latest")
    BRI = helper('BRI', "https://www.abs.gov.au/ausstats/meisubs.nsf/log?openagent&63020013c.xls&6302.0&Time%20Series%20Spreadsheet&53D3812E37D68499CA2583A700120CA2&0&Nov%202018&21.02.2019&Latest")
    ADE = helper('ADE', "https://www.abs.gov.au/ausstats/meisubs.nsf/log?openagent&63020013d.xls&6302.0&Time%20Series%20Spreadsheet&D670A7700F39964CCA2583A700120D0F&0&Nov%202018&21.02.2019&Latest")
    PER = helper('PER', "https://www.abs.gov.au/ausstats/meisubs.nsf/log?openagent&63020013e.xls&6302.0&Time%20Series%20Spreadsheet&A81063864555FB99CA2583A700120D78&0&Nov%202018&21.02.2019&Latest")
    CAN = helper('CAN', "https://www.abs.gov.au/ausstats/meisubs.nsf/log?openagent&63020013h.xls&6302.0&Time%20Series%20Spreadsheet&6D98F9BF2DBA6075CA2583A700120EBB&0&Nov%202018&21.02.2019&Latest")
    HOB = helper('HOB', "https://www.abs.gov.au/ausstats/meisubs.nsf/log?openagent&63020013f.xls&6302.0&Time%20Series%20Spreadsheet&B03D471731F53F4CCA2583A700120DE2&0&Nov%202018&21.02.2019&Latest")
    DAR = helper('DAR', "https://www.abs.gov.au/ausstats/meisubs.nsf/log?openagent&63020013g.xls&6302.0&Time%20Series%20Spreadsheet&BCD4E42986763012CA2583A700120E51&0&Nov%202018&21.02.2019&Latest")

    seriess = [SYD, MEL, BRI, ADE, PER, CAN, HOB, DAR]
    df = reduce(lambda left,right: pd.merge(left,right, left_index=True, right_index=True), seriess)
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d")

    existing = pd.read_csv(os.path.join(BASE_DIR,f"../media_files/datasets/annualincome.csv"), index_col=0)
    existing.index = pd.to_datetime(existing.index, format="%Y-%m-%d")

    new = pd.concat((existing, df[df.index > existing.index[-1]]))
    new.to_csv(os.path.join(BASE_DIR,f"../media_files/datasets/annualincome.csv"))


def update_allords_PE_ratio():
    """
    Scrapes marketindex website for historical Allords price earnings ratio (dimensionless).
    """

    tr=TorRequest(password='mywealthanalyst_admin')
    tr.reset_identity() # Reset Tor
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent,}

    current_ip = tr.get('http://ipecho.net/plain').text

    url = 'https://www.marketindex.com.au/sites/default/files/statistics/asx-fundamentals.xlsx'
    r = tr.get(url, headers=headers)

    filepath = os.path.join(BASE_DIR,f"../media_files/datasets/allordsperatio_askprice_avg_aud.csv")

    with open(os.path.join(BASE_DIR,f"../media_files/datasets/asx-fundamentals.xlsx"), 'wb') as f:
        f.write(r.content)

    df = pd.read_excel(os.path.join(BASE_DIR,f"../media_files/datasets/asx-fundamentals.xlsx"), header=9)

    df = df[['Date','PE Ratio']]
    df.columns = ['Date','AskPrice_Avg_AUD']
    df.dropna(axis=0,how='any',inplace=True)

    df.to_csv(filepath, index=False)
