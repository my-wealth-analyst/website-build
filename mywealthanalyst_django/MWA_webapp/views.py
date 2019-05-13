from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from mywealthanalyst_django.settings import BASE_DIR
import pandas as pd
import numpy as np
import os
import requests

# from .forms import commodity_dropdown_field
from .models import Commodities

# Create your views here.

def get_current_movement(commodity=None):
    filepath = os.path.join(BASE_DIR, f"../media_files/datasets/{commodity}_askprice_avg_aud.csv")
    df = pd.read_csv(filepath)


    last_price = df.AskPrice_Avg_AUD.values[len(df.AskPrice_Avg_AUD.values)-1]
    second_last_price = df.AskPrice_Avg_AUD.values[len(df.AskPrice_Avg_AUD.values)-2]

    if last_price > second_last_price:
        increase = 1
    elif last_price < second_last_price:
        increase = -1
    elif last_price == second_last_price:
        increase = 0

    return({'last_price':last_price, 'increase':increase})

def home(request):
    # form = commodity_dropdown_field()
    form_options = Commodities.objects.values_list('commodity_name', flat=True)

    gold = get_current_movement('gold')
    silver = get_current_movement('silver')

    return render(request, 'MWA_webapp/main.html', {'gold':gold, 'silver':silver, 'form_options':form_options})


def get_data(request):
    commodity_one = request.GET.get('commodity_one', None)
    commodity_two = request.GET.get('commodity_two', None)

    filepath_one = os.path.join(BASE_DIR, f"../media_files/datasets/{commodity_one}_askprice_avg_aud.csv")
    filepath_two = os.path.join(BASE_DIR, f"../media_files/datasets/{commodity_two}_askprice_avg_aud.csv")

    try:
        commodity_one_df = pd.read_csv(filepath_one)
        commodity_one_df.columns = ['Date',commodity_one]
        commodity_one_df = commodity_one_df.set_index('Date')
        commodity_one_df.sort_index(axis=0,ascending=True,inplace=True)
        commodity_one_df = commodity_one_df.loc[~commodity_one_df.index.duplicated(keep='first')]

        commodity_two_df = pd.read_csv(filepath_two)
        commodity_two_df.columns = ['Date',commodity_one]
        commodity_two_df = commodity_two_df.set_index('Date')
        commodity_two_df.sort_index(axis=0,ascending=True,inplace=True)
        commodity_two_df = commodity_two_df.loc[~commodity_two_df.index.duplicated(keep='first')]


        df = commodity_one_df.merge(commodity_two_df, left_index=True,right_index=True)
        df.dropna(axis=0,how='any',inplace=True)

        if df[df.columns[0]].sum() > df[df.columns[1]].sum():  # if commodity one nominally 'more valuable' (i.e. higher number) than commodity two
            df['output'] = df[df.columns[0]] / df[df.columns[1]]
        else: # if commodity two nominally 'more valuable' (i.e. higher number) than commodity one
            df['output'] = df[df.columns[1]] / df[df.columns[0]]

        df.reset_index(inplace=True)
        df = df[['Date','output']]
        df.Date = pd.to_datetime(df.Date)
        df.Date = df.Date.astype(np.int64) // 10**6

        df.columns = ['x','y']

        df_jsonformat = [df.values.tolist()]

        return HttpResponse(df_jsonformat)

    except ValueError:
        return HttpResponse([], content_type = 'application/json')
