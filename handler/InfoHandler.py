from MsgId import MsgId
from handler.Handler import Handler
from storage import Storage


class InfoHandler(Handler):

    def __init__(self, storage: Storage):
        super(InfoHandler, self).__init__([MsgId.SESSION_OPEN])
        self._storage = storage

    def _handle(self, wsapp, json_msg):
        for clazz in json_msg['classList']:
            if (clazz['ccode']) == 'QJSIM':
                instruments = list(
                    map(lambda x: Instrument(x['scode'], x['sname'], x['long_name'], x['lot'], x['step'], x['scale']),
                        clazz['secList']))
                self._storage.save(instruments)


class Instrument:

    def __init__(self, scode=None, sname=None, long_name=None, lot=None, step=None, scale=0):
        self.__name = sname
        self.__long_name = long_name
        self.__code = scode
        self.__lot_size = lot
        self.__priceStep = step
        self.__scale = scale

    @property
    def code(self):
        return self.__code

    @property
    def name(self):
        return self.__name

    @property
    def lot_size(self):
        return self.__lot_size

    @property
    def step(self):
        return (1 / (10 ** self.__scale)) * self.__priceStep

    @property
    def full_name(self):
        return self.__long_name
