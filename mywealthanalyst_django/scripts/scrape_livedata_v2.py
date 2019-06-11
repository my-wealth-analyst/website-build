from bs4 import BeautifulSoup
from MWA_webapp.models import Commodities
from datetime import datetime

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

from MWA_webapp.apps import driver


def helper(soup=None, title=None):
    base_element = soup.find("a",{'title':title})
    price = base_element.findNext('td')
    price_change = price.findNext('td')
    price_change_perc = price_change.findNext('td')

    price = float(price.text.replace(",", ""))
    price_change = float(price_change.text.replace(",", ""))
    price_change_perc = float(price_change_perc.text.replace("%", ""))

    return({'price': price, 'price_change': price_change, 'price_change_perc': price_change_perc})


def scrape_current(driver=driver):
    # First check for and close any popups (turns out this isn't even necessary)
    # try:
    #     element = driver.find_element_by_xpath("//i[@class='popupCloseIcon largeBannerCloser']")
    #     element.click()
    # except:
    #     pass

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    AUD = helper(soup=soup, title='AUD/USD - Australian Dollar US Dollar')

    OIL_USD = helper(soup=soup, title='Crude Oil WTI Futures (CFD)')
    GOLD_USD = helper(soup=soup, title='Gold Futures (CFD)')
    SILVER_USD = helper(soup=soup, title='Silver Futures (CFD)')
    BITCOIN_USD = helper(soup=soup, title='BTC/USD - Bitcoin US Dollar')

    ALLORDS_AUD = helper(soup=soup, title='ASX All Ordinaries')
    ALLORDS_USD = ALLORDS_AUD
    ALLORDS_USD["price"] = ALLORDS_USD["price"]*AUD["price"]
    ALLORDS_USD["price_change"] = ALLORDS_USD["price_change"]*AUD["price"]


    Commodities.objects.filter(commodity_name="AUD").update(date_last_scraped=datetime.now(),
                                                                 last_price=AUD["price"],
                                                                 last_movement_nominal=AUD["price_change"],
                                                                 last_movement_percentage=AUD["price_change_perc"])

    Commodities.objects.filter(commodity_name="Oil").update(date_last_scraped=datetime.now(),
                                                                 last_price=OIL_USD["price"],
                                                                 last_movement_nominal=OIL_USD["price_change"],
                                                                 last_movement_percentage=OIL_USD["price_change_perc"])

    Commodities.objects.filter(commodity_name="Gold").update(date_last_scraped=datetime.now(),
                                                                 last_price=GOLD_USD["price"],
                                                                 last_movement_nominal=GOLD_USD["price_change"],
                                                                 last_movement_percentage=GOLD_USD["price_change_perc"])

    Commodities.objects.filter(commodity_name="Silver").update(date_last_scraped=datetime.now(),
                                                                 last_price=SILVER_USD["price"],
                                                                 last_movement_nominal=SILVER_USD["price_change"],
                                                                 last_movement_percentage=SILVER_USD["price_change_perc"])

    Commodities.objects.filter(commodity_name="Bitcoin").update(date_last_scraped=datetime.now(),
                                                                 last_price=BITCOIN_USD["price"],
                                                                 last_movement_nominal=BITCOIN_USD["price_change"],
                                                                 last_movement_percentage=BITCOIN_USD["price_change_perc"])

    Commodities.objects.filter(commodity_name="All Ords").update(date_last_scraped=datetime.now(),
                                                                 last_price=ALLORDS_USD["price"],
                                                                 last_movement_nominal=ALLORDS_USD["price_change"],
                                                                 last_movement_percentage=ALLORDS_USD["price_change_perc"])
