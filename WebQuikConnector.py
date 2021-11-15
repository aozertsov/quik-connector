import time
from enum import Enum
from threading import Thread as _Thread

from websocket import WebSocketConnectionClosedException

from MsgId import MsgId
import websocket
import json
import logging

log = logging.getLogger(__name__)


class WebQuikConnector:
    _handlers = {}

    class Status(Enum):
        CONNECTING = 0
        INITIALIZING = 1
        INITIALIZED = 2
        BUSY = 3
        DISCONNECTING = 4
        DISCONNECTED = 5

    def __init__(self, url, login, password, version, origin):

        self._conn = url
        self._password = password
        self._login = login
        self._version = version
        self._origin = origin
        self._status = self.Status.DISCONNECTED
        self._callbacks = {
            MsgId.TRADE_SESSION_OPEN: self._on_trade_session_open,
            MsgId.CLASSES_SENT: self._on_classes_sent,
        }
        self.__prepare_ws()

    def __prepare_ws(self):
        self._ws = websocket.WebSocketApp(self._conn,
                                          subprotocols=["dumb-increment-protocol"],
                                          header={
                                              "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits"},
                                          on_close=self._on_close,
                                          on_open=self._on_socket_open,
                                          on_message=self._on_message,
                                          on_error=self._on_error,
                                          on_pong=self._on_pong,
                                          on_ping=self._on_ping)
        self._t = _Thread(target=self._ws.run_forever, kwargs={"origin": self._origin, "ping_interval": 6})
        self._t.daemon = True

    # region socket standard funs
    def _on_error(self, wsapp, error):
        log.error("Got Error: {}".format(error), exc_info=True)

    def _on_message(self, wsapp, raw_msg):
        """
        Entry for message processing. Call specific processors for different messages.
        """
        strmsg = raw_msg.decode()
        msg = json.loads(strmsg)

        # Call internal callback is set up
        msg_callback = self._callbacks.get(msg['msgid'])
        if msg_callback:
            # Don't send msg to consumers, process it in this class
            msg_callback(msg)

        if self._handlers.get(msg['msgid']):
            for handler in self._handlers[msg['msgid']]:
                handler.handle(wsapp, msg)

    def _on_close(self, wsapp, close_status_code, close_msg):
        log.warning("Connection closed with message: {}".format(close_msg))

    def _on_pong(self, wsapp, message):
        request = {"msgid": MsgId.ACTIVITY}
        self._ws.send(json.dumps(request))

    def _on_ping(self, wsapp, message):
        log.info("Got a ping! Message: {}".format(message))

    def _on_socket_open(self, ws):
        log.info("Socket connection opening")
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
        try:
            self._ws.send(json.dumps(request))
        except WebSocketConnectionClosedException as cce:
            log.error(f'Connection closed with exception: {cce}')
            self._status = self.Status.DISCONNECTED
            raise cce

    # endregion

    def _on_trade_session_open(self, msg):
        """
        Trade session is opened. Now we can request data and set orders
        """
        if msg['resultCode'] == 0:
            log.info('Authenticated')
            self._status = WebQuikConnector.Status.INITIALIZING
            log.info('Connected. Trade session is opened')
        else:
            # Not opened, failure failed
            self._status = WebQuikConnector.Status.DISCONNECTED
            raise ConnectionError('Trade session opening failure: %s' % msg)

    def _on_classes_sent(self, msg):
        self._status = WebQuikConnector.Status.INITIALIZED

    def start(self):
        self._status = self.Status.CONNECTING
        self._t.start()

    def send_message(self, message):
        log.info(f'message {message} sent')
        self._ws.send(json.dumps(message))

    def add_handler(self, handler):
        for msg_id in handler.message_ids:
            if self._handlers.get(msg_id):
                self._handlers[msg_id].append(handler)
            else:
                self._handlers[msg_id] = [handler]

    # region Common requests
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
    # endregion
