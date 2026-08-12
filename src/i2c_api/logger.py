from abc import ABC, abstractmethod

from i2c_api.log import I2CTransactionElement

class I2CLogger(ABC):
    @abstractmethod
    def log_message(self, message: list[I2CTransactionElement]):
        pass