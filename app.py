from time import sleep
from lib import config, scheduler


if config["environment"] == "development":
    schedule = scheduler.register_test_schedule()
else:
    schedule = scheduler.register_schedule()

while True:
    schedule.run_pending()
    sleep(1)
