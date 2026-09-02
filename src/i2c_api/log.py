from bitstring import Bits


class I2CTransactionElement:
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class START(I2CTransactionElement):
    pass


class STOP(I2CTransactionElement):
    pass


class RESTART(I2CTransactionElement):
    pass


class READ(I2CTransactionElement):
    pass


class WRITE(I2CTransactionElement):
    pass


class ACK(I2CTransactionElement):
    pass


class NACK(I2CTransactionElement):
    pass


class DATA_MOSI(I2CTransactionElement):
    __match_args__ = ("payload",)

    def __init__(self, payload: Bits):
        self.payload = payload

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.payload})"


class DATA_MISO(I2CTransactionElement):
    __match_args__ = ("payload",)

    def __init__(self, payload: Bits):
        self.payload = payload

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.payload})"


class I2CMessage:
    START = START()
    STOP = STOP()
    RESTART = RESTART()
    READ = READ()
    WRITE = WRITE()
    ACK = ACK()
    NACK = NACK()
    DATA_MOSI = DATA_MOSI
    DATA_MISO = DATA_MISO
