import requests
import json
from datetime import datetime


def print_result(message):
    print("%s: %s" % (datetime.now(), message))


class APIClientException(BaseException):
    pass


class APIClient:
    def __init__(self):
        self.base_url = "http://localhost:5000"

    def feed_now(self):
        url = "%s/feeder/feed_now" % self.base_url
        response = requests.post(url)
        print_result(response.json())

    def set_lights(self, power):
        url = "%s/lighting" % self.base_url
        data = dict(power=power)
        response = requests.put(url, data=json.dumps(data))
        print_result(response.json())

    def lights_on(self):
        self.set_lights(True)

    def lights_off(self):
        self.set_lights(False)

    def lights_status(self):
        url = "%s/lighting" % self.base_url
        response = requests.get(url)
        print_result(response.json())

    def light_on_feed(self):
        self.feed_now()
        self.lights_on()
