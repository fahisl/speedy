import json
from flask import Flask, request, make_response
from lib import SerialClient, Feeder, FeederException, Lighting, config

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


@api.route("/lighting", methods=["PUT"])
def basking_lights_on():
    result = None
    try:
        body = request.get_json()
        requested_power = body["power"]
        if not requested_power:
            result = lighting.power_off()
        else:
            result = lighting.power_on()
    except Exception as e:
        return json_response({"message": str(e), "error": True}, 400)

    return json_response(result)


@api.route("/lighting", methods=["GET"])
def basking_lights_status():
    return json_response(lighting.status())


if __name__ == '__main__':
    speedy_board_id = "speedy"
    speedy_board = SerialClient(config["boards"][speedy_board_id]["port"], speedy_board_id)
    speedy_board.connect()
    print("Speedy board connected")
    feeder = Feeder(speedy_board)
    lighting = Lighting(speedy_board)
    api.run(debug=True)
