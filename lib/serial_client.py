from serial import Serial
from time import sleep
import json


class SerialClientException(BaseException):
    pass


class SerialClient:
    def __init__(self, port, client_id, baudrate=9600):
        self.board = None
        self.port = port
        self.baudrate = baudrate
        self.client_id = client_id

    def connect(self):
        self.board = Serial(port=self.port, baudrate=self.baudrate)
        sleep(3)

        # Board verification
        response = self.read()
        if response.get("status") != "ready":
            raise SerialClientException("Invalid response while connecting to %s board: %s" % (self.client_id, response))

        reported_id = self.board_id()
        if reported_id != self.client_id:
            raise SerialClientException("Connected to wrong board: id = %s" % reported_id)

    def board_id(self):
        return self.write("ident;", 1).get("id")

    def write(self, data, read_delay=3):
        self.flush_serial()
        self.board.write(data.encode("utf-8"))
        sleep(read_delay)
        return self.read()

    def flush_serial(self):
        self.read()

    def read(self):
        out = ''
        while self.board.inWaiting() > 0:
            out += self.board.read().decode("utf-8")

        try:
            response = json.loads(out)
        except Exception as e:
            response = dict()

        return response
