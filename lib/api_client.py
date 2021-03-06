import requests
import logging
from lib.config import config


class APIClientException(BaseException):
    pass


class APIClient:
    def __init__(self):
        self.base_url = "http://%s:%s" % (config["api"]["host"], config["api"]["port"])

    def feed_now(self):
        url = "%s/feeder/feed_now" % self.base_url
        response = requests.post(url)
        logging.info(response.json())

    def lights_on(self):
        url = "%s/lighting/on" % self.base_url
        response = requests.post(url)
        logging.info(response.json())

    def lights_off(self):
        url = "%s/lighting/off" % self.base_url
        response = requests.post(url)
        logging.info(response.json())

    def lights_status(self):
        url = "%s/lighting" % self.base_url
        response = requests.get(url)
        logging.info(response.json())

    def light_on_feed(self):
        self.feed_now()
        self.lights_on()
