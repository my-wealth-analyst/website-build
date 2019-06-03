from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from scripts.scrape_livedata import scrape_all
from scripts.get_historical_data import update_gold_and_silver, update_oil, update_bitcoin, update_allords_PE_ratio, update_allords

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/5')),
    name="update_live_prices",
    ignore_result=True
)
def update_live_prices():
    """
    Scrape live prices (to be run every 5 minutes)
    """
    try:
        scrape_all()
        logger.info("Live prices updated")

    except Exception as exc:
        # overrides the default delay to retry after 1 minute
        raise self.retry(exc=exc, countdown=60, max_retries=2)

@periodic_task(
    run_every=(crontab(minute=0, hour=0)),
    name="update_historical_prices",
    ignore_result=True
)
def update_historical_prices():
    """
    Scrape live prices (to be run every 5 minutes)
    """
    try:
        update_gold_and_silver()
        update_oil()
        update_bitcoin()
        update_allords_PE_ratio()
        update_allords()
        logger.info("Historical prices updated")

    except Exception as exc:
        # overrides the default delay to retry after 1 minute
        raise self.retry(exc=exc, countdown=60, max_retries=2)
