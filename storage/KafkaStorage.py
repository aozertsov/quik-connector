import json
from abc import ABC

from kafka import KafkaProducer

from storage.Storage import Storage


class KafkaStorage(Storage, ABC):

    def __init__(self,
                 bootstrap_servers='localhost:9092',
                 key_serializer=str.encode,
                 value_serializer=lambda v: json.dumps(v).encode('utf-8')):
        self._producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                       key_serializer=key_serializer,
                                       value_serializer=value_serializer)
