from MsgId import MsgId
from handler.Handler import Handler
from storage import Storage


class ClassesHandler(Handler):
    """
    Handler, which works with Securities groupped by classes.
    """

    def __init__(self, storage: Storage):
        super(ClassesHandler, self).__init__([MsgId.CLASSES])
        self._storage = storage

    def _handle(self, wsapp, json_msg):
        self._storage.save(json_msg['classList'][0])
