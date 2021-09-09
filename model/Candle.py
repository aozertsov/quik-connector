from datetime import datetime


class Candle:

    def __init__(self, d=None, o=None, c=None, h=None, l=None, v=None):
        self._date = datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
        self._open = o
        self._close = c
        self._high = h
        self._low = l
        self._volume = v

    @property
    def date(self):
        return self._date

    @property
    def open(self):
        return self._open

    @property
    def close(self):
        return self._close

    @property
    def high(self):
        return self._high

    @property
    def low(self):
        return self._low

    @property
    def volume(self):
        return self._volume

    def __str__(self):
        return f'{{"date": "{self._date}", "open": {self.open}, close: {self.close}, high: {self.high}, low: {self.low}, volume: {self.volume}}}'

    def __repr__(self):
        return f'{{"date": "{self._date}", "open": {self.open}, close: {self.close}, high: {self.high}, low: {self.low}, volume: {self.volume}}}'