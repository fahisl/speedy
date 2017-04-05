import schedule
from datetime import datetime, timedelta
from lib import tasks, config


def register_test_schedule():
    print("Building test schedule")
    current_time = datetime.now()

    job_time_1 = (current_time + timedelta(seconds=60)).strftime("%H:%M")
    schedule.every().day.at(job_time_1).do(tasks.light_on_feed)
    print("Feeding and lights-on scheduled at %s" % job_time_1)

    job_time_2 = (current_time + timedelta(seconds=120)).strftime("%H:%M")
    schedule.every().day.at(job_time_2).do(tasks.basking_lights_off)
    print("Lights off scheduled at %s" % job_time_2)

    return schedule


def register_schedule():
    print("Registering schedule from config")
    schedule_config = config["schedule"]

    lights_on = schedule_config.get("lights_on")
    if lights_on:
        schedule.every().day.at(lights_on).do(tasks.basking_lights_on)
        print("Lights on scheduled at %s" % lights_on)

    lights_off = schedule_config.get("lights_off")
    if lights_off:
        schedule.every().day.at(lights_off).do(tasks.basking_lights_off)
        print("Lights off scheduled at %s" % lights_off)

    lights_status_interval = schedule_config.get("lights_status_interval")
    if lights_status_interval:
        schedule.every(lights_status_interval).minutes.do(tasks.basking_lights_status)
        print("Lights status check scheduled every %s minutes" % lights_status_interval)

    feeding_interval = schedule_config.get("feeding_interval")
    feeding_time = schedule_config.get("feeding_time")
    if feeding_interval and feeding_time:
        schedule.every(feeding_interval).days.at(feeding_time).do(tasks.feed)
        print("Feeding scheduled every %s days at %s" % (feeding_interval, feeding_time))

    return schedule
