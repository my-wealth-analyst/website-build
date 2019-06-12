from django.apps import AppConfig



class MwaWebappConfig(AppConfig):
    name = 'MWA_webapp'
    verbose_name = "MyWealthAnalyst Django Web App"

    def ready(self):
        pass
