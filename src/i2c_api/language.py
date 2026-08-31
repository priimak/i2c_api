"""
Following code is prototype to be compeleted.
"""

from typing import Self

from i2c_api.master import I2CMaster


class Command:
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class S(Command):
    pass


class Address(Command):
    def __init__(self, address: int):
        self.address = address

    def __repr__(self) -> str:
        if self.address == -1:
            return f"{self.__class__.__name__}(auto)"
        else:
            return f"{self.__class__.__name__}(0x{self.address:02X})"


class Address10(Command):
    def __init__(self, address: int):
        self.address = address

    def __repr__(self) -> str:
        if self.address == -1:
            return f"{self.__class__.__name__}(auto)"
        else:
            return f"{self.__class__.__name__}(0x{self.address:02X})"


class R(Command):
    pass


class W(Command):
    pass


class Data(Command):
    def __init__(self, data: int):
        self.data = data

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(0x{self.data:02X})"


class Read(Command):
    def __init__(self, num_bytes: int):
        self.num_bytes = num_bytes

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.num_bytes})"


class Sr(Command):
    pass


class P(Command):
    pass


class I2CStopStart:
    def __init__(self, i2c: "I2C"):
        self._i2c = i2c

    def stop(self) -> "I2C":
        self._i2c._i2c_commands.append(P())
        return self._i2c.clone_and_clear()

    def restart(self) -> "I2CAddress":
        self._i2c._i2c_commands.append(Sr())
        return I2CAddress(self._i2c)


class I2CMoreData(I2CStopStart):
    def __init__(self, i2c: "I2C"):
        super().__init__(i2c)

    def data(self, data: int | list[int]) -> Self:
        if isinstance(data, int):
            self._i2c._i2c_commands.append(Data(data))
        else:
            for b in data:
                self._i2c._i2c_commands.append(Data(b))
        return self


class I2CData:
    def __init__(self, i2c: "I2C"):
        self._i2c = i2c

    def data(self, data: int | list[int]) -> I2CMoreData:
        if isinstance(data, int):
            self._i2c._i2c_commands.append(Data(data))
        else:
            for b in data:
                self._i2c._i2c_commands.append(Data(b))
        return I2CMoreData(self._i2c)


class I2CReadWrite:
    def __init__(self, i2c: "I2C"):
        self._i2c = i2c

    def read(self, number_of_bytes: int) -> I2CStopStart:
        self._i2c._i2c_commands.append(Read(number_of_bytes))
        return I2CStopStart(self._i2c)

    def write(self) -> I2CData:
        self._i2c._i2c_commands.append(W())
        return I2CData(self._i2c)


class I2CAddress:
    def __init__(self, i2c: "I2C"):
        self._i2c = i2c

    def address(self, device_address: int = -1) -> I2CReadWrite:
        self._i2c._i2c_commands.append(Address(device_address))
        return I2CReadWrite(self._i2c)

    def address10(self, device_address: int = -1) -> I2CReadWrite:
        raise RuntimeError("Not implemented")
        # self._i2c._i2c_commands.append(Address10(device_address))
        # return I2CReadWrite(self._i2c)


class I2C:
    def __init__(self, master: I2CMaster | None = None):
        self._master = master
        self._i2c_commands = []

    def start(self) -> I2CAddress:
        self._i2c_commands.append(S())
        return I2CAddress(self)

    def exec(
        self, master: I2CMaster | None = None, device_address: int = -1
    ) -> tuple[list[list[int]], bool]:
        if self._master is None and master is None:
            raise ValueError("I2CMaster must be provided to execute this transaction")

        if device_address == -1:
            for c in self._i2c_commands:
                if isinstance(c, Address) and c.address == -1:
                    raise ValueError(
                        "Some Address(...) commands are given without address. "
                        "Thus, argument `address` must be provided."
                    )

        return [], True

    def __repr__(self) -> str:
        return "i2c." + ".".join(str(c) for c in self._i2c_commands)

    def clone_and_clear(self) -> "I2C":
        i2c = I2C(self._master)
        i2c._i2c_commands = self._i2c_commands.copy()
        self._i2c_commands.clear()
        return i2c


if __name__ == "__main__":
    i2c = I2C()
    a = i2c.start().address().write().data(0x7).data(0xA1).stop()
    data, is_success = (
        i2c.start()
        .address(22)
        .write()
        .data(0x8)
        .restart()
        .address(0x6)
        .read(5)
        .stop()
        .exec()
    )

    print(a)
    print(data)
