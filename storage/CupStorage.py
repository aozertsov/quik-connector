from datetime import datetime

from model.Cup import Cup
from storage.KafkaStorage import KafkaStorage


class CupStorage(KafkaStorage):

    def flush(self):
        pass

    def __init__(self, bootstrap_servers='localhost:9092'):
        super(CupStorage, self).__init__(bootstrap_servers, value_serializer=lambda x: str(x).encode())
        self._cup_storage = dict()

    def save(self, kvp):
        (key, value) = kvp
        v = Cup(value['lines'], datetime.now())
        try:
            self._producer.send("cup", key=key, value=v)
        except Exception as e:
            print(e)
        self._cup_storage[key] = value
