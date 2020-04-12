from abc import ABC, abstractmethod


class Handler(ABC):
    """
    Abstract method describe logic of handling messages from quik server
    """

    __message_id = 0

    def __init__(self, message_id):
        self.__message_id = message_id

    def handle(self, json_msg):
        if json_msg['msgid'] == self.__message_id:
            self._handle(json_msg)

    @property
    def message_id(self):
        return self.__message_id

    @abstractmethod
    def _handle(self, json_msg):
        pass