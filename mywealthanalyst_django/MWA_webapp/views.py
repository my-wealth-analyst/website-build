from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from mywealthanalyst_django.settings import BASE_DIR
import pandas as pd
import numpy as np
import os
import requests

from .models import Commodities

# Create your views here.

def landingpage(request):

    return render(request, 'MWA_webapp/landingpage.html')


@login_required
def dashboard(request):

    All = Commodities.objects.filter(enabled=True)
    Gold = Commodities.objects.filter(enabled=True).get(commodity_name='Gold')
    Silver = Commodities.objects.filter(enabled=True).get(commodity_name='Silver')
    Property = Commodities.objects.filter(enabled=True).get(commodity_name='Property')
    Oil = Commodities.objects.filter(enabled=True).get(commodity_name='Oil')
    AllOrds = Commodities.objects.filter(enabled=True).get(commodity_name='All Ordinaries')
    Bitcoin = Commodities.objects.filter(enabled=True).get(commodity_name='Bitcoin')
    AUD = Commodities.objects.get(commodity_name='Australian Dollar')

    return render(request, 'MWA_webapp/main.html', {'Commodities':All , 'Gold':Gold, 'Silver': Silver , 'Property':Property , 'Oil':Oil , 'AllOrds':AllOrds , 'Bitcoin':Bitcoin, 'AUD':AUD })

@login_required(redirect_field_name='my_redirect_field')
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
