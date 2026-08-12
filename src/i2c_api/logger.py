from abc import ABC, abstractmethod

from .log import I2CTransactionElement


class I2CLogger(ABC):
    @abstractmethod
    def log_message(self, message: list[I2CTransactionElement]):
        pass
