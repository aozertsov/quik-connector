import time

import Config
from WebQuikConnector import WebQuikConnector
from handler.CandleHandler import CandleHandler
from handler.CupHandler import CupHandler
from handler.InfoHandler import InfoHandler
from handler.TickerHandler import TickerHandler
from storage.CandleStorage import CandleStorage
from storage.CupStorage import CupStorage
from storage.InfoStorage import InfoStorage
from storage.TickerStorage import TickerStorage

connector = WebQuikConnector(url=Config.WSS,
                             login=Config.LOGIN,
                             password=Config.PASSWORD,
                             version=Config.QUIK_VERSION,
                             origin=Config.ORIGIN)


def main():
    cup_storage = CupStorage(bootstrap_servers='kafka-server1:29092')
    ticker_storage = TickerStorage(bootstrap_servers='kafka-server1:29092')
    candle_storage = CandleStorage(bootstrap_servers='kafka-server1:29092')

    ticker = TickerHandler(ticker_storage)
    plotter = CandleHandler(candle_storage)
    cup_handler = CupHandler(cup_storage)
    info_handler = InfoHandler(InfoStorage())

    connector.add_handler(plotter)
    connector.add_handler(cup_handler)
    connector.add_handler(ticker)
    connector.add_handler(info_handler)
    connector.start()

    connector.ask_bottle('SBER')
    connector.candles('SBER', 1)

    # smth like daemon run
    while True:
        time.sleep(10)


if __name__ == '__main__':
    import logging

    logging.basicConfig(filename='application.log',
                        format='%(asctime)s: %(levelname)s - %(name)s - %(filename)s.%(funcName)s%(lineno)d - '
                               '%(message)s',
                        level=logging.INFO)
    main()
