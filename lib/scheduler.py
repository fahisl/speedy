import schedule
import logging
from datetime import datetime, timedelta
from lib import config, APIClient

api_client = APIClient()


def register_test_schedule():
    logging.info("Building test schedule")
    current_time = datetime.now()

    job_time_1 = (current_time + timedelta(seconds=60)).strftime("%H:%M")
    schedule.every().day.at(job_time_1).do(api_client.lights_on)
    logging.info("Feeding and lights-on scheduled at %s" % job_time_1)

    job_time_2 = (current_time + timedelta(seconds=120)).strftime("%H:%M")
    schedule.every().day.at(job_time_2).do(api_client.lights_off)
    logging.info("Lights off scheduled at %s" % job_time_2)

    schedule.every(30).seconds.do(api_client.lights_status)
    schedule.every().minute.do(api_client.feed_now)

    return schedule


def register_status_checker():
    logging.info("Building status checker schedule")
    schedule.every(30).seconds.do(api_client.lights_status)
    logging.info("Schedule is registered")
    return schedule


def register_schedule():
    logging.info("Registering schedule from config")
    schedule_config = config["schedule"]

    lights_on = schedule_config.get("lights_on")
    if lights_on:
        schedule.every().day.at(lights_on).do(api_client.lights_on)
        logging.info("Lights on scheduled at %s" % lights_on)

    lights_off = schedule_config.get("lights_off")
    if lights_off:
        schedule.every().day.at(lights_off).do(api_client.lights_off)
        logging.info("Lights off scheduled at %s" % lights_off)

    lights_status_interval = schedule_config.get("lights_status_interval")
    if lights_status_interval:
        schedule.every(lights_status_interval).minutes.do(api_client.lights_status)
        logging.info("Lights status check scheduled every %s minutes" % lights_status_interval)

    feeding_interval = schedule_config.get("feeding_interval")
    feeding_time = schedule_config.get("feeding_time")
    if feeding_interval and feeding_time:
        schedule.every(feeding_interval).days.at(feeding_time).do(api_client.feed_now)
        logging.info("Feeding scheduled every %s days at %s" % (feeding_interval, feeding_time))

    return schedule
