from scraper.main_scraper import update_stored_records
from schedule import every, repeat, run_pending
import time

@repeat(every(1).day)
def update_records_job():
    
    update_stored_records()

while True:
    run_pending()
    time.sleep(1)
