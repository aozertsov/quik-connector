class Cup:

    def __init__(self, lines=None, timestamp=None):
        self._timestamp = timestamp
        buys = list(filter(lambda x: int(x[1]['b']) > 0, lines.items()))
        asks = list(filter(lambda x: int(x[1]['s']) > 0, lines.items()))
        self._buys = list(map(lambda x: CupElement('buy', x[0], x[1]['b']), buys))
        self._sells = list(map(lambda x: CupElement('sell', x[0], x[1]['s']), asks))
        a = 10

    def __str__(self):
        return f'{{"timestamp": {self._timestamp}, "buys": {self._buys}, "sells": {self._sells} }}'


class CupElement:

    def __init__(self, type, price, count):
        self._type = type
        self._count = count
        self._price = price

    def __str__(self):
        return f'{{"type": {self._type}, "count": {self._count}, "price": {self._price} }}'

    def __repr__(self):
        return f'{{"type": {self._type}, "count": {self._count}, "price": {self._price} }}'
