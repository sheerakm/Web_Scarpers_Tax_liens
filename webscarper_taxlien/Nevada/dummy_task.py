from celery import Celery
import time
import random

celery = Celery(__name__)
celery.config_from_object('celeryconfig')

@celery.task
def run_scraper(script_id: int):
    # Dummy scraper
    print(f"Running scraper {script_id}")
    time.sleep(random.randint(1, 3))
    return f"Scraper {script_id} completed"
