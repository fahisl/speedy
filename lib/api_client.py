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

    def lights_on(self):
        url = "%s/lighting/on" % self.base_url
        response = requests.post(url)
        print_result(response.json())

    def lights_off(self):
        url = "%s/lighting/off" % self.base_url
        response = requests.post(url)
        print_result(response.json())

    def lights_status(self):
        url = "%s/lighting" % self.base_url
        response = requests.get(url)
        print_result(response.json())

    def light_on_feed(self):
        self.feed_now()
        self.lights_on()
