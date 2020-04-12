from handler.Handler import Handler
from storage import Storage
from storage.TickerStorage import TickerStorage


class TickerHandler(Handler):
    """
    Handler, which works with ticks from quik server
    """

    def __init__(self, storage: Storage):
        super(TickerHandler, self).__init__(21011)
        self._dict = {}
        self._storage = storage

    def _handle(self, json_msg):
        self._storage.save(json_msg['dataResult'])