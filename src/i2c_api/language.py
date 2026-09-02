from typing import Self

from bitstring import BitArray

from i2c_api.commands import Address, Command, Data, P, Read, S, Sr, W
from i2c_api.master import I2CMaster


class I2CStopStart:
    def __init__(self, i2c: "I2CTransaction"):
        self._i2c = i2c

    def stop(self) -> "I2CTransaction":
        self._i2c._i2c_commands.append(P())
        return self._i2c

    def restart(self) -> "I2CAddress":
        self._i2c._i2c_commands.append(Sr())
        return I2CAddress(self._i2c)


class I2CMoreData(I2CStopStart):
    def __init__(self, i2c: "I2CTransaction"):
        super().__init__(i2c)

    def data(self, data: int | list[int]) -> Self:
        if isinstance(data, int):
            self._i2c._i2c_commands.append(Data(data))
        else:
            for b in data:
                self._i2c._i2c_commands.append(Data(b))
        return self


class I2CData:
    def __init__(self, i2c: "I2CTransaction"):
        self._i2c = i2c

    def data(self, data: int | list[int]) -> I2CMoreData:
        if isinstance(data, int):
            self._i2c._i2c_commands.append(Data(data))
        else:
            for b in data:
                self._i2c._i2c_commands.append(Data(b))
        return I2CMoreData(self._i2c)


class I2CReadWrite:
    def __init__(self, i2c: "I2CTransaction"):
        self._i2c = i2c

    def read(self, number_of_bytes: int) -> I2CStopStart:
        self._i2c._i2c_commands.append(Read(number_of_bytes))
        return I2CStopStart(self._i2c)

    def write(self) -> I2CData:
        self._i2c._i2c_commands.append(W())
        return I2CData(self._i2c)


class I2CAddress:
    def __init__(self, i2c: "I2CTransaction"):
        self._i2c = i2c

    def address(self, device_address: int = -1) -> I2CReadWrite:
        self._i2c._i2c_commands.append(Address(device_address))
        return I2CReadWrite(self._i2c)

    def address10(self, device_address: int = -1) -> I2CReadWrite:
        raise RuntimeError("Not implemented")


class I2CTransaction:
    def __init__(self, master: I2CMaster | None = None):
        self._master = master
        self._i2c_commands: list[Command] = []

    def start(self) -> I2CAddress:
        new_root = I2CTransaction()
        new_root._i2c_commands.append(S())
        return I2CAddress(new_root)

    def exec(
        self, master: I2CMaster | None = None, device_address: int = -1
    ) -> tuple[list[list[BitArray]], bool]:
        if self._master is None and master is None:
            raise ValueError("I2CMaster must be provided to execute this transaction")

        if device_address == -1:
            for c in self._i2c_commands:
                if isinstance(c, Address) and c.address == -1:
                    raise ValueError(
                        "Some Address(...) commands are given without address. "
                        "Thus, argument `address` must be provided."
                    )

        master_to_use = self._master if master is None else master
        return master_to_use.exec(self)

    def __repr__(self) -> str:
        return "i2c." + ".".join(str(c) for c in self._i2c_commands)
