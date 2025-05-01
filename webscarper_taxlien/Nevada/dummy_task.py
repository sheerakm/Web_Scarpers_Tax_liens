from celery import Celery
import time

celery = Celery(__name__)
celery.config_from_object('celeryconfig')

@celery.task
def run_scraper(script_id: int):
    # Dummy scraper
    print(f"Running scraper {script_id}")
    time.sleep(3500)
    return f"Scraper {script_id} completed"


