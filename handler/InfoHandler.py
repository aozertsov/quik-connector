from handler.Handler import Handler
from storage import Storage


class InfoHandler(Handler):

    def __init__(self, storage: Storage):
        super(InfoHandler, self).__init__(20000)
        self._storage = storage

    def _handle(self, json_msg):
        for clas in json_msg['classList']:
            if (clas['ccode']) == 'QJSIM':
                print(clas['secList'])