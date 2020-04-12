import time

import Config
from WebQuikConnector import WebQuikConnector
from handler.CandleHandler import CandleHandler
from handler.CupHandler import CupHandler
from handler.TickerHandler import TickerHandler
from storage.CandleStorage import CandleStorage
from storage.CupStorage import CupStorage
from storage.TickerStorage import TickerStorage

connector = WebQuikConnector(url=Config.URL, login=Config.LOGIN, password=Config.PASSWORD)


def main():
    cup_storage = CupStorage()
    ticker_storage = TickerStorage()
    candle_storage = CandleStorage()

    ticker = TickerHandler(ticker_storage)
    plotter = CandleHandler(candle_storage)
    cup_handler = CupHandler(cup_storage)

    connector.add_handler(plotter)
    connector.add_handler(cup_handler)
    connector.add_handler(ticker)
    connector.start()

    connector.ask_bottle('SBER')
    connector.candles('SBER', 1)

    # smth like daemon run
    while True:
        time.sleep(10)


if __name__ == '__main__':
    main()
