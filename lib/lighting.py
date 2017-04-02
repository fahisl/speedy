class LightingException(BaseException):
    pass


class Lighting:
    def __init__(self, serial_client):
        self.board = serial_client

    def status(self):
        return self.board.write("lights.status;", read_delay=1)

    def power_on(self):
        return self.board.write("lights.on;", read_delay=1)

    def power_off(self):
        return self.board.write("lights.off;", read_delay=1)
