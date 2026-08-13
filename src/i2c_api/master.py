from abc import ABC, abstractmethod

from bitstring import BitArray, Bits

from .logger import I2CLogger


class I2CMaster(ABC):
    @staticmethod
    def mk_payload(data: Bits | str | int | list[int]) -> BitArray:
        if isinstance(data, int):
            return BitArray(f"uint:8={data}")
        elif isinstance(data, list):
            acc = BitArray(0)
            for b in data:
                acc += BitArray(f"uint:8={b}")
            return acc
        elif isinstance(data, str) or isinstance(data, Bits):
            return BitArray(data)
        else:
            raise RuntimeError("Invalid payload type")

    @staticmethod
    def pad_payload(payload: BitArray, num_bytes: int | None = None) -> Bits:
        if num_bytes is None:
            if payload.len % 8 != 0:
                payload.prepend(BitArray(8 - payload.len % 8))
            else:
                return payload

        elif payload.len > num_bytes * 8:
            payload = payload[-(num_bytes * 8) :]

        elif payload.len < num_bytes * 8:
            payload.prepend(BitArray(num_bytes * 8 - payload.len))

        return payload

    @abstractmethod
    def logger(self) -> I2CLogger:
        pass

    @abstractmethod
    def write(
        self,
        address: int,
        data: Bits | str | int | list[int],
        num_bytes: int | None = None,
    ) -> bool:
        """
        Performs write transaction sending `data` to the target device identified by `address`. At the end master will
        issue Stop condition and will release the clock line.

        :param address: i2c address of the target device
        :param data: array of bits to send to the target device; if int or list[int], then these are assumed to be bytes
        :param num_bytes: number of bytes to send or if None, then send all bits in `data` padded with zero bits.
        :return: True or False indicating if write succeeded, which is that client responded with ACK bits.
        """

    @abstractmethod
    def read(self, address: int, num_bytes: int = 1) -> Bits | None:
        """
        Performs read transaction reading `num_bytes` (default is 1) from the target device identified by `address`.
        At the end master will issue Stop condition and will release the clock line.

        :param address: i2c address of the target device
        :param num_bytes: number of bytes to read
        :return: None if failed to read data from the client (that is client did not send ACK bits) or data is Bits
        """

    @abstractmethod
    def read_register(
        self, address: int, register: int, num_bytes: int = 1, use_restart: bool = True
    ) -> Bits | None:
        """
        Reads register from the target device identified by `address`. This is a compound operation where we
        send first `write(address, register, num_bytes=1)` followed by `read(address, register, num_bytes)`.
        If `use_restart` is True (default), then if device supports it i2c restart will be used between read and write
        operations and if device does not support it them RuntimeError will be raised. if `use_restart` is False, then
        two separate transactions will be used to perform register read operation with clock line being released between
        them.

        :param address: i2c address of the target device
        :param register: address of the register to read
        :param num_bytes: number of bytes to read; this should match length of the register
        :param use_restart: True or False (default) indicating if we should try using I2C restart op between read and
                write operations
        :return: None if at any point during these transactions client sends NACK or actual Bits holding response data
        """

    @abstractmethod
    def write_register(
        self,
        address: int,
        register: int,
        data: Bits | str | int | list[int],
        num_bytes: int | None = 1,
        read_back: bool = False,
    ) -> BitArray | None:
        """
        Writes register to the target device. This is basically same as `write(...)` where first write byte is register
        address and subsequent bytes are values to write into a register.

        :param address: i2c address of the target device
        :param register: address of the register to write to
        :param data: array of bits to send to the target device; if int or list[int], then these are assumed to be bytes
        :param num_bytes: number of bytes to send or if None, then send all bits in `data` padded with zero bits.
        :param read_back: if True, then register read operation will be performed at the end and its value returned.
            Otherwise, if False (default), then just do write and return back to the user the same BitArray that was
            supplied to this function as `data`.
        :return: Value written into the register or None of NACK was received at any moment from the client device.
        """

    @abstractmethod
    def scan(self) -> list[int]:
        """
        Scans for all client devices connected on this I2C bus.

        :return: list of addresses of connected devices
        """

    @abstractmethod
    def list_pullups(self) -> list[str]:
        """
        Returns list of possible configurable pullup resistor values.
        These should be human-readable values like [20 OHm]
        """

    @abstractmethod
    def set_pullup(self, pullup_value: str) -> None:
        """
        Set pullup resistor value. This should be one of the strings returned by `list_pullups()` method.
        """

    @abstractmethod
    def get_pullup(self) -> str:
        """
        Returns currently active pullup resistor value in human-readable format.
        """

    @abstractmethod
    def list_clk_speeds(self) -> list[int]:
        """Returns list of available configuable clock speeds in KHz."""

    @abstractmethod
    def get_clk_speed(self) -> int:
        """Returns currently configued clock speed in KHz."""

    @abstractmethod
    def set_clk_speed(self, speed: int) -> None:
        """
        Sets clock speed to `speed` value in KHz. Supplied value must be one of the returned one by
        method `list_clk_speeds()`, if not, then RuntimeError is raised.
        """
