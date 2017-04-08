import json
import logging
from flask import Flask, request, make_response
from lib import SerialClient, Feeder, FeederException, Lighting, config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
api = Flask(__name__)
feeder = None
lighting = None


def json_response(data, status=200, serialize=True):
    header = {
        "Content-Type": "application/json",
        "Cache-Control": "no-store"
    }

    if serialize is True:
        return make_response((json.dumps(data), status, header))
    else:
        return make_response((data, status, header))


@api.route("/feeder/feed_now", methods=["POST"])
def feed_now():
    try:
        result = feeder.feed_now()
        return json_response(result)

    except FeederException as e:
        result = {"error": True, "message": str(e)}
        return json_response(result, 400)


@api.route("/feeder/reset", methods=["POST"])
def feeder_reset():
    return json_response(feeder.reset())


@api.route("/lighting/on", methods=["POST"])
def basking_lights_on():
    return json_response(lighting.power_on())


@api.route("/lighting/off", methods=["POST"])
def basking_lights_off():
    return json_response(lighting.power_off())


@api.route("/lighting", methods=["GET"])
def basking_lights_status():
    return json_response(lighting.status())


if __name__ == '__main__':
    speedy_board_id = "speedy"
    speedy_board = SerialClient(config["boards"][speedy_board_id]["port"], speedy_board_id)
    speedy_board.connect()
    logging.info("Speedy board connected")
    feeder = Feeder(speedy_board)
    lighting = Lighting(speedy_board)
    api.run(debug=False, host="0.0.0.0")
