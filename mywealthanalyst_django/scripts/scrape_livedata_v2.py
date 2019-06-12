from bs4 import BeautifulSoup
from MWA_webapp.models import Commodities
from datetime import datetime
from django.conf import settings

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

# from MWA_webapp.apps import driver
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument('user-agent={0}'.format(user_agent))
# if settings.DEBUG:
#     options.headless = False
# else:
#     options.headless = True
options.headless = True



class BrowserSession(object):
    def __init__(self):
        # self.driver = webdriver.Firefox(executable_path=r'geckodriver.exe', options=options)
        self.driver = webdriver.Firefox(executable_path=r'./geckodriver', options=options)
        self.driver.get('https://au.investing.com/?ref=www')
        print("Driver started")


def helper(soup=None, title=None):
    base_element = soup.find("a",{'title':title})
    price = base_element.findNext('td')
    price_change = price.findNext('td')
    price_change_perc = price_change.findNext('td')

    price = float(price.text.replace(",", ""))
    price_change = float(price_change.text.replace(",", ""))
    price_change_perc = float(price_change_perc.text.replace("%", ""))

    return({'price': price, 'price_change': price_change, 'price_change_perc': price_change_perc})


def scrape_current():
    global Driver_Live
    try:
        Driver
    except:
        Driver = BrowserSession()

    # First check for and close any popups (turns out this isn't even necessary)
    # try:
    #     element = driver.find_element_by_xpath("//i[@class='popupCloseIcon largeBannerCloser']")
    #     element.click()
    # except:
    #     pass

    soup = BeautifulSoup(Driver.driver.page_source, 'html.parser')

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
