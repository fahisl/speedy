import logging
from time import sleep
from lib import config, scheduler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

if config["environment"] == "development":
    schedule = scheduler.register_status_checker()
else:
    schedule = scheduler.register_schedule()

while True:
    schedule.run_pending()
    sleep(1)
