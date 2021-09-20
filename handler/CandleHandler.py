from MsgId import MsgId
from handler.Handler import Handler
from storage import Storage


class CandleHandler(Handler):
    """
    Handler to work with candles from server
    """

    def __init__(self, storage: Storage):
        super(CandleHandler, self).__init__([MsgId.GRAPH])
        self._storage = storage

    def _handle(self, wsapp, json_msg):
        graphs = json_msg['graph']
        self._storage.save(graphs)
