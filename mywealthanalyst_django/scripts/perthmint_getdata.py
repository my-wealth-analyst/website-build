import pandas as pd
import numpy as np
import os
from mywealthanalyst_django.settings import BASE_DIR
import matplotlib.pyplot as plt


def delete_commodity_file(commodity = None):
    filepath = os.path.join(BASE_DIR,f"../media_files/datasets/{commodity}_askprice_avg_aud.csv")
    if os.path.isfile(filepath):
        os.remove(filepath)

def data_update_commodity(commodity = None):

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

data_update_commodity('gold')
data_update_commodity('gold')
data_update_commodity('silver')
data_update_commodity('silver')
