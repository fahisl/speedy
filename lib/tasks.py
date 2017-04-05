from datetime import datetime
from lib import Feeder, FeederException
from lib import Lighting
from lib import SerialClient
from lib import config


def initialize():
    speedy_board_id = "speedy"
    speedy_board = SerialClient(config["boards"][speedy_board_id]["port"], speedy_board_id)
    speedy_board.connect()
    print("Speedy board connected")
    return Feeder(speedy_board), Lighting(speedy_board)


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


feeder, lighting = initialize()
