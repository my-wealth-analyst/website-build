from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from scripts.scrape_livedata_v2 import scrape_current
from scripts.get_historical_data_v2 import update_houseprice, update_annualincome

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/5')),
    name="cron_update_live_prices",
    ignore_result=True
)
def cron_update_live_prices():
    """
    Scrape live prices (to be run every 5 minutes)
    """
    try:
        scrape_current()
    except Exception as exc:
        logger.warning(exc)
        raise Exception


@periodic_task(
    run_every=(crontab(0, 0, day_of_month='1', month_of_year='*/1')),
    name="cron_update_houseprice_and_annualincome",
    ignore_result=True
)
def cron_update_houseprice_and_annualincome():
    """
    Update ABS house price data for 8 capital cities
    """
    update_houseprice()
    update_annualincome()
