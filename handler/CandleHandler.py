from handler.Handler import Handler
from storage import Storage
from storage.CandleStorage import CandleStorage


class CandleHandler(Handler):
    """
    Handler to work with candles from server
    """

    def __init__(self, storage: Storage):
        super(CandleHandler, self).__init__([21016])
        self._storage = storage

    def _handle(self, json_msg):
        graphs = json_msg['graph']
        self._storage.save(graphs)