from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from mywealthanalyst_django.settings import BASE_DIR
import pandas as pd
import numpy as np
import os
import requests

from .models import Commodities

from scripts.get_historical_data import update_allords

# Create your views here.


def landingpage(request):
    return render(request, 'MWA_webapp/landingpage.html')


@login_required
def dashboard(request):

    All = Commodities.objects.order_by('display_order').filter(enabled=True)
    Gold = Commodities.objects.filter(enabled=True).get(commodity_name='Gold')
    Silver = Commodities.objects.filter(enabled=True).get(commodity_name='Silver')
    Property = Commodities.objects.filter(enabled=True).get(commodity_name='Property')
    Oil = Commodities.objects.filter(enabled=True).get(commodity_name='Oil')
    AllOrds = Commodities.objects.filter(enabled=True).get(commodity_name='All Ords')
    Bitcoin = Commodities.objects.filter(enabled=True).get(commodity_name='Bitcoin')
    AUD = Commodities.objects.get(commodity_name='AUD')

    return render(request, 'MWA_webapp/main.html', {'Commodities': All, 'Gold': Gold, 'Silver': Silver,
    'Property':Property , 'Oil': Oil , 'AllOrds': AllOrds , 'Bitcoin': Bitcoin, 'AUD': AUD
    })


@login_required(redirect_field_name='my_redirect_field')
def get_data(request):
    commodity_one = request.GET.get('commodity_one', None)
    commodity_two = request.GET.get('commodity_two', None)
    city = request.GET.get('city', None)

    filepath_one = os.path.join(BASE_DIR, f"../media_files/datasets/{commodity_one}.csv")
    filepath_two = os.path.join(BASE_DIR, f"../media_files/datasets/{commodity_two}.csv")

    commodity_one_df = pd.read_csv(filepath_one, index_col=0)
    commodity_one_df.index = pd.to_datetime(commodity_one_df.index)
    commodity_one_df.sort_index(axis=0,ascending=True,inplace=True)

    if commodity_one == 'houseprice':
        if city:
            commodity_one_df = commodity_one_df[[city]]
            commodity_one_df = commodity_one_df.resample('d').interpolate(method='linear')
        else:
            return HttpResponse()

    commodity_one_df = commodity_one_df.loc[~commodity_one_df.index.duplicated(keep='first')]

    if commodity_two == 'identity':
        commodity_two_df = commodity_one_df.copy()
        commodity_two_df.iloc[:] = 1
    else:
        commodity_two_df = pd.read_csv(filepath_two, index_col=0)
        commodity_two_df.index = pd.to_datetime(commodity_two_df.index)
        commodity_two_df.sort_index(axis=0,ascending=True,inplace=True)

        if commodity_two == 'annualincome':
            if city:
                commodity_two_df = commodity_two_df[[city]]*52
                commodity_two_df = commodity_two_df.resample('d').interpolate(method='linear')
            else:
                return HttpResponse()

        commodity_two_df = commodity_two_df.loc[~commodity_two_df.index.duplicated(keep='first')]

    commodity_one_df = commodity_one_df.resample('d').interpolate(method='linear')
    commodity_two_df = commodity_two_df.resample('d').interpolate(method='linear')

    df = commodity_one_df.merge(commodity_two_df, left_index=True,right_index=True)
    df = df.replace(0, np.nan)
    df.dropna(axis=0, how='any',inplace=True)

    df['output'] = df[df.columns[0]] / df[df.columns[1]]

    df.reset_index(inplace=True)
    df = df[['Date','output']]
    df.Date = pd.to_datetime(df.Date)
    df.Date = df.Date.astype(np.int64) // 10**6

    df.columns = ['x','y']
    df_jsonformat = [df.values.tolist()]
    return HttpResponse(df_jsonformat)
