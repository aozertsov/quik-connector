from typing import List

from handler.InfoHandler import Instrument
from storage.Storage import Storage


class InfoStorage(Storage):

    def __init__(self):
        self._instruments = dict()

    def save(self, instruments: List[Instrument]):
        for instrument in instruments:
            self._instruments[instrument.code] = instrument

    def flush(self):
        pass

    def get_info(self, code: str):
        return self._instruments[code]
