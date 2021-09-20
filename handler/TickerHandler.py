from MsgId import MsgId
from handler.Handler import Handler
from storage import Storage


class TickerHandler(Handler):
    """
    Handler, which works with ticks from quik server
    """

    def __init__(self, storage: Storage):
        super(TickerHandler, self).__init__([MsgId.TICKER])
        self._dict = {}
        self._storage = storage

    def _handle(self, wsapp, json_msg):
        self._storage.save(json_msg['dataResult'])
