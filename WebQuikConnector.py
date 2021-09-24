from threading import Event
from threading import Thread as _Thread
import websocket
import json
import time


class WebQuikConnector:
    _handlers = {}

    def __init__(self, url, login, password, version, origin):

        self._conn = url
        self._password = password
        self._login = login
        self._version = version
        self._origin = origin
        self._ws = websocket.WebSocketApp(self._conn,
                                          subprotocols=["dumb-increment-protocol"],
                                          header={
                                              "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits"},
                                          on_close=self._on_close,
                                          on_open=self._on_socket_open,
                                          on_message=self._on_message,
                                          on_error=self._on_error)
        self._t = _Thread(target=self._ws.run_forever, kwargs={"origin": self._origin})
        self._t.daemon = True
        self._thread_for_ping = _Thread(target=self.__quik_run_forever)
        self._thread_for_ping.daemon = True

    def __quik_run_forever(self):
        ticker = Event()
        while not ticker.wait(3):
            self._on_ping()

    #region socket standard funs
    def _on_error(self, wsapp, error):
        print("startend")
        print(type(error))

    def _on_message(self, wsapp, raw_msg):
        """
        Entry for message processing. Call specific processors for different messages.
        """
        strmsg = raw_msg.decode()
        msg = json.loads(strmsg)

        print(msg)

        if self._handlers.get(msg['msgid']):
            for handler in self._handlers[msg['msgid']]:
                handler.handle(wsapp, msg)

    def _on_close(self, wsapp, close_status_code, close_msg):
        print('connection closed')

    def _on_socket_open(self, ws):
        print("startup")
        request = {
            "msgid": 10000,
            "login": self._login,
            "password": self._password,
            "classes": [],
            "btc": "true",
            "app_type": "WEB",
            "version": self._version,
            "userAgent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0",
            "height": "498",
            "width": "1920",
            # "compressed": "deflate", Do not uncomment this line to prevent problems with message encoding
            "sid": "bf71",
            "ccodeOnDepo": "false"
        }
        self._ws.send(json.dumps(request))
    #endregion

    def start(self):
        self._t.start()
        time.sleep(10)
        self._thread_for_ping.start()

    def send_message(self, message):
        self._ws.send(json.dumps(message))

    def add_handler(self, handler):
        for msg_id in handler.message_ids:
            if self._handlers.get(msg_id):
                self._handlers[msg_id].append(handler)
            else:
                self._handlers[msg_id] = [handler]

    #region Common requests
    def ask_bottle(self, scode, depth=15):
        request = {
            "msgid": 11014,
            "c": "QJSIM",
            "s": scode,
            "depth": depth
        }
        self.send_message(request)

    def send_order(self, scode, price, quantity, is_sell=False):
        is_sell_num = 1 if is_sell else 0
        order = {
            "msgid": 12000,
            "isMarket": 0,
            "isMarketSpread": 0,
            "spread": "0",
            "price": f'{price}',
            "takeProfit": "0",
            "offset": "0",
            "isStop": "0",
            "ccode": "QJSIM",
            "scode": f'{scode}',
            "account": "NL0011100043",
            "clientCode": "13222",
            "sell": f'{is_sell_num}',
            "quantity": f'{quantity}'
        }
        self.send_message(order)

    def candles(self, scode, interval):
        request = {
            "msgid": 11016,
            "c": "QJSIM",
            "s": scode,
            "p": interval
        }
        self.send_message(request)
    #endregion