from MsgId import MsgId
from handler.Handler import Handler
from storage import Storage


class CupHandler(Handler):
    """
    Handler, which works with Cup of asks and bids from server.
    """

    def __init__(self, storage: Storage):
        super(CupHandler, self).__init__([MsgId.CUP])
        self._storage = storage

    def _handle(self, wsapp, json_msg):
        for (k, v) in json_msg['quotes'].items():
            if not v == {}:
                self._storage.save((k, v))
