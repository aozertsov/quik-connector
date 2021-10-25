from datetime import datetime

from model.Candle import Candle
from storage.KafkaStorage import KafkaStorage


class CandleStorage(KafkaStorage):

    def __init__(self, bootstrap_servers='localhost:29092'):
        super(CandleStorage, self).__init__(bootstrap_servers=bootstrap_servers,
                                            value_serializer=lambda x: str(x).encode())
        self._last_candle_date = dict()
        self._dict = dict()
        self._counter = dict()
        self._flush_num = 10

    def flush(self):
        pass

    def save(self, candles_map):
        for instrument in candles_map.keys():

            if instrument in self._last_candle_date:
                last_date = self._last_candle_date[instrument]
                income_candles = list(filter(lambda x: datetime.strptime(x['d'], '%Y-%m-%d %H:%M:%S') > last_date, candles_map[instrument]))
                candles_to_send = list(map(lambda x: Candle(**x), income_candles))
            else:
                candles_to_send = list(map(lambda x: Candle(**x), candles_map[instrument]))

            self._last_candle_date[instrument] = candles_to_send[len(candles_to_send) - 1].date
            for value in candles_to_send:
                try:
                    self._producer.send("candle", key=instrument, value=value)
                except Exception as e:
                    print(e)
