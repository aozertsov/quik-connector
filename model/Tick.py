class Tick:

    def __init__(self, bid=None, offer=None, last=None, lastchange=None):
        self._bid = bid
        self._offer = offer
        self._last = last
        self._lastchange = lastchange

    @property
    def bid(self):
        return self._bid

    @bid.setter
    def bid(self, bid):
        self._bid = bid

    @property
    def offer(self):
        return self._offer

    @offer.setter
    def bid(self, offer):
        self._offer = offer

    @property
    def last(self):
        return self._last

    @last.setter
    def last(self, last):
        self._last = last

    @property
    def lastchange(self):
        return self._lastchange

    @lastchange.setter
    def last(self, lastchange):
        self._lastchange = lastchange

    def __str__(self):
        return f'{{bid: {self.bid}, offer: {self.offer}}}'
