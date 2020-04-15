from handler.InfoHandler import Instrument
from storage.Storage import Storage


class InfoStorage(Storage):

    def __init__(self):
        self._instruments = dict()

    def save(self, instruments: list()):
        for instrument in instruments:
            self._instruments[instrument.code] = instrument

    def flush(self):
        pass

    def getInfo(self, code: str):
        return self._instruments[code]
