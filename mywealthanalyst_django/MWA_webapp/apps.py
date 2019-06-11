from django.apps import AppConfig

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.conf import settings

class MwaWebappConfig(AppConfig):
    name = 'MWA_webapp'
    verbose_name = "MyWealthAnalyst Django Web App"

    def ready(self):

        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if settings.DEBUG:
            options.headless = False
        else:
            options.headless = True
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument('user-agent={0}'.format(user_agent))

        global driver
        # driver = webdriver.Chrome(chrome_options=options)
        driver = None
        page = driver.get('https://au.investing.com/?ref=www')
