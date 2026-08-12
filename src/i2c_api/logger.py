from abc import ABC, abstractmethod

from bitstring import Bits


class I2CTransactionElement:
    pass

class START:
    pass

class STOP:
    pass

class RESTART:
    pass

class ACK:
    pass

class NACK:
    pass

class DATA_MOSI:
    __match_args__ = ("payload",)

    def __init__(self, payload: Bits):
        self.payload = payload

class DATA_MISO:
    __match_args__ = ("payload",)

    def __init__(self, payload: Bits):
        self.payload = payload

class I2CLogger(ABC):
    @abstractmethod
    def log_message(self, message: list[I2CTransactionElement]):
        pass