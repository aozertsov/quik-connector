from abc import ABC, abstractmethod
from typing import List


class Handler(ABC):
    """
    Abstract method describe logic of handling messages from quik server
    """

    __message_ids = []

    def __init__(self, message_ids: List[int]):
        self.__message_ids = message_ids

    def handle(self, wsapp, json_msg):
        if self.__message_ids and json_msg['msgid'] in self.__message_ids:
            self._handle(wsapp, json_msg)

    @property
    def message_ids(self):
        return self.__message_ids

    @abstractmethod
    def _handle(self, wsapp, json_msg):
        pass