class FeederException(BaseException):
    pass


class Feeder:
    def __init__(self, serial_client):
        self.board = serial_client

    def feed_now(self):
        if not self.remaining_feeds():
            raise FeederException("Cannot feed: feeder is empty")
        return self.board.write('feeder.feed;')

    def remaining_feeds(self):
        return self.status().get("remaining_feeds")

    def status(self):
        return self.board.write('feeder.status;', read_delay=1)

    def reset(self):
        return self.board.write('feeder.reset;')
