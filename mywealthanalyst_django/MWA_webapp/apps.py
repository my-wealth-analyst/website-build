from django.apps import AppConfig

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.conf import settings
from pyvirtualdisplay import Display
from selenium import webdriver

class MwaWebappConfig(AppConfig):
    name = 'MWA_webapp'
    verbose_name = "MyWealthAnalyst Django Web App"

    def ready(self):

        display = Display(visible=0, size=(800, 600))
        display.start()

        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # if settings.DEBUG:
        #     options.headless = False
        # else:
        #     options.headless = True
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument('user-agent={0}'.format(user_agent))

        global driver
        driver = None
        # driver = webdriver.Chrome(chrome_options=options)
        # print(driver)
        # page = driver.get('https://au.investing.com/?ref=www')
        print(page)
