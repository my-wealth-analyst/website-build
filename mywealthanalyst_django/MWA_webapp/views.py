from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from mywealthanalyst_django.settings import BASE_DIR
import pandas as pd
import numpy as np
import os
import requests

from .models import Commodities, Commodity_TS

from scripts.get_historical_data import update_allords

# Create your views here.


def landingpage(request):
    return render(request, 'MWA_webapp/landingpage.html')


@login_required
def dashboard(request):
    AUD_LAST_PRICE = Commodity_TS.objects.filter(
        name__iexact='AUD').latest('date').last_price

    user = request.user
    if user.activated == False:
        return render(request, 'MWA_users/email_not_activated.html')

    All = Commodities.objects.order_by('display_order').filter(enabled=True)

    Gold = Commodity_TS.objects.filter(name__iexact="Gold").latest('date')
    Silver = Commodity_TS.objects.filter(name__iexact="Silver").latest('date')
    Oil = Commodity_TS.objects.filter(name__iexact="Oil").latest('date')
    AllOrds = Commodity_TS.objects.filter(
        name__iexact="AllOrds").latest('date')
    Bitcoin = Commodity_TS.objects.filter(
        name__iexact="Bitcoin").latest('date')
    AUD = Commodity_TS.objects.filter(name__iexact="AUD").latest('date')

    # Gold = Commodities.objects.filter(
    #     enabled=True).filter(commodity_name='Gold').first()
    # Silver = Commodities.objects.filter(
    #     enabled=True).filter(commodity_name='Silver').first()
    # Oil = Commodities.objects.filter(
    #     enabled=True).filter(commodity_name='Oil').first()
    # AllOrds = Commodities.objects.filter(enabled=True).filter(
    #     commodity_name='All Ords').first()
    # Bitcoin = Commodities.objects.filter(
    #     enabled=True).filter(commodity_name='Bitcoin').first()
    # AUD = Commodities.objects.filter(commodity_name='AUD').first()

    Property = pd.read_csv(os.path.join(
        BASE_DIR, f"../media_files/datasets/houseprice.csv"), index_col=0)
    Property.index = pd.to_datetime(Property.index)
    try:
        Property = Property*1000 * AUD_LAST_PRICE
    except AttributeError:
        pass
    Property = Property.iloc[-1, :]

    return render(request, 'MWA_webapp/main.html', {'Gold': Gold, 'Silver': Silver,
                                                    'Property': Property, 'Oil': Oil, 'Allords': AllOrds, 'Bitcoin': Bitcoin, 'AUD': AUD
                                                    })


@login_required(redirect_field_name='my_redirect_field')
def get_propertyprice(request):

    AUD_LAST_PRICE = Commodity_TS.objects.filter(
        name__iexact='AUD').latest('date').last_price

    user = request.user
    if user.activated == False:
        return render(request, 'MWA_users/email_not_activated.html')

    city = request.GET.get('city', None)
    AUD = Commodities.objects.get(commodity_name='AUD')

    Property = pd.read_csv(os.path.join(
        BASE_DIR, f"../media_files/datasets/houseprice.csv"), index_col=0)
    Property = Property*1000 * AUD_LAST_PRICE
    Property = Property.iloc[-1, :]
    return HttpResponse(Property[city])


@login_required(redirect_field_name='my_redirect_field')
def get_data(request):
    user = request.user
    if user.activated == False:
        return render(request, 'MWA_users/email_not_activated.html')

    commodity_one = request.GET.get('commodity_one', None)
    commodity_two = request.GET.get('commodity_two', None)
    city = request.GET.get('city', None)

    commodity_one_df = Commodity_TS.objects.filter(
        name__iexact=commodity_one).to_timeseries(index='date')
    commodity_one_df = commodity_one_df.drop('datetime', axis=1)

    if commodity_one == 'houseprice':
        filepath_one = os.path.join(
            BASE_DIR, f"../media_files/datasets/{commodity_one}.csv")
        commodity_one_df = pd.read_csv(filepath_one, )
        commodity_one_df.Date = pd.to_datetime(
            commodity_one_df.Date, format="%d/%m/%Y")
        commodity_one_df.set_index('Date', inplace=True)
        commodity_one_df.sort_index(axis=0, ascending=True, inplace=True)

        if city:
            commodity_one_df = commodity_one_df[[city]]
            commodity_one_df = commodity_one_df.resample(
                'd').interpolate(method='linear')
            commodity_one_df = commodity_one_df*1000

            exch = Commodity_TS.objects.filter(
                name__iexact="AUD").to_timeseries(index='date')
            exch = exch.drop('datetime', axis=1)
            exch = exch.resample('d').interpolate(method='linear')
            commodity_one_df = commodity_one_df.merge(
                exch, left_index=True, right_index=True)

            commodity_one_df.last_price = commodity_one_df.iloc[:,
                                                                0] * commodity_one_df.last_price
            commodity_one_df.index = commodity_one_df.index.rename('date')

        else:
            return HttpResponse()

    commodity_one_df = commodity_one_df.loc[~commodity_one_df.index.duplicated(
        keep='first')]

    if commodity_two == 'identity':
        commodity_two_df = commodity_one_df.copy()
        commodity_two_df.iloc[:] = 1

    else:
        commodity_two_df = Commodity_TS.objects.filter(
            name__iexact=commodity_two).to_timeseries(index='date')
        commodity_two_df = commodity_two_df.drop('datetime', axis=1)

        if commodity_two == 'annualincome':
            filepath_two = os.path.join(
                BASE_DIR, f"../media_files/datasets/{commodity_two}.csv")
            commodity_two_df = pd.read_csv(filepath_two)
            commodity_two_df.Date = pd.to_datetime(
                commodity_two_df.Date, format="%d/%m/%Y")
            commodity_two_df.set_index('Date', inplace=True)
            commodity_two_df.sort_index(axis=0, ascending=True, inplace=True)

            if city:
                commodity_two_df = commodity_two_df[[city]]*52
                commodity_two_df = commodity_two_df.resample(
                    'd').interpolate(method='linear')

                exch = Commodity_TS.objects.filter(
                    name__iexact="AUD").to_timeseries(index='date')
                exch = exch.drop('datetime', axis=1)
                exch = exch.resample('d').interpolate(method='linear')

                commodity_two_df = commodity_two_df.merge(
                    exch, left_index=True, right_index=True)
                commodity_two_df.last_price = commodity_two_df.iloc[:,
                                                                    0] * commodity_two_df.last_price
                commodity_two_df.index = commodity_two_df.index.rename('date')

            else:
                return HttpResponse()

        commodity_two_df = commodity_two_df.loc[~commodity_two_df.index.duplicated(
            keep='first')]

    commodity_one_df = commodity_one_df.resample(
        'd').interpolate(method='linear')
    commodity_two_df = commodity_two_df.resample(
        'd').interpolate(method='linear')

    commodity_one_df = commodity_one_df[['name', 'last_price']]
    commodity_two_df = commodity_two_df[['name', 'last_price']]

    df = commodity_one_df.merge(
        commodity_two_df, left_index=True, right_index=True)
    df = df.replace(0, np.nan)
    df.dropna(axis=0, how='any', inplace=True)

    df['output'] = df.last_price_x / df.last_price_y
    df.reset_index(inplace=True)

    df = df[['date', 'output']]
    df.date = pd.to_datetime(df.date)
    df.date = df.date.astype(np.int64) // 10**6

    df.columns = ['x', 'y']
    df_jsonformat = [df.values.tolist()]
    return HttpResponse(df_jsonformat)


def testview(request):
    return render(request, 'MWA_users/confirmation_email.html')
