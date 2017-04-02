import schedule
import time
from datetime import datetime, timedelta
from lib import config, SerialClient, Feeder, FeederException, Lighting


def print_result(result):
    print("%s %s" % (datetime.now(), result))


def feed():
    try:
        result = feeder.feed_now()
        print_result(result)
    except FeederException as e:
        print_result(e)


def basking_lights_on():
    result = lighting.power_on()
    print_result(result)


def basking_lights_off():
    result = lighting.power_off()
    print_result(result)


def basking_lights_status():
    result = lighting.status()
    print_result(result)


def light_on_feed():
    basking_lights_on()
    feed()


def register_schedule(test=False):
    if test:
        current_time = datetime.now()
        job_time_1 = (current_time + timedelta(seconds=60)).strftime("%H:%M")
        job_time_2 = (current_time + timedelta(seconds=120)).strftime("%H:%M")
        schedule.every().day.at(job_time_1).do(light_on_feed)
        schedule.every().day.at(job_time_2).do(basking_lights_off)
        return

    schedule.every(2).days.at("06:15").do(feed)
    schedule.every().day.at("06:00").do(basking_lights_on)
    schedule.every().day.at("20:00").do(basking_lights_off)
    schedule.every(30).minutes.do(basking_lights_status)


speedy_board_id = "speedy"
speedy_board = SerialClient(config["boards"][speedy_board_id]["port"], speedy_board_id)
speedy_board.connect()
feeder = Feeder(speedy_board)
lighting = Lighting(speedy_board)
feeder.reset()
print("Speedy board connected")

register_schedule(test=config["environment"] == "development")
print("Schedule is registered")

while True:
    schedule.run_pending()
    time.sleep(1)
