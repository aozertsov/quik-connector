import json

from kafka import KafkaProducer

from model.Tick import Tick
from storage.KafkaStorage import KafkaStorage


class TickerStorage(KafkaStorage):

    def __init__(self, bootstrap_servers = 'localhost:9092'):
        super(TickerStorage, self).__init__(bootstrap_servers, value_serializer = lambda x: str(x).encode())
        self._dict = dict()

    def save(self, data):
        for (k, v) in data.items():
            self._dict[k] = Tick(**v)
            try:
                self._producer.send("ticker", key=k, value=self._dict[k])
            except Exception as e:
                print(e)

    def flush(self):
        pass
