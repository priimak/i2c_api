from abc import ABC, abstractmethod

from bitstring import Bits, BitArray


class I2CMaster(ABC):
    @abstractmethod
    def write(self, address: int, data: Bits | str | int, num_bytes: int | None = None) -> bool:
        """
        Performs write transaction sending `data` to the target device identified by `address`.

        :param address: i2c address of the target device
        :param data: array of bits to send to the target device.
        :param num_bytes: number of bytes to send or if None, then send all bits in `data` padded with zero bits.
        :return: True or False indicating if write succeeded, which is that client responded with ACK bits.
        """

    @abstractmethod
    def read(self, address: int, num_bytes: int = 1) -> Bits | None:
        """
        Performs read transaction reading `num_bytes` (default is 1) from the target device identified by `address`.

        :param address: i2c address of the target device
        :param num_bytes: number of bytes to read
        :return: None if failed to read data from the client (that is client did not send ACK bits) or data is Bits
        """

    @abstractmethod
    def read_register(self, address: int, register: int, num_bytes: int = 1, use_restart: bool = False) -> Bits | None:
        """
        Reads register from the target device identified by `address`. This is a compound operation where we
        send first `write(address, register, num_bytes=1)` followed by `read(address, register, num_bytes)`.
        If `use_restart` is True then if device supports it i2c restart will be used between read and write operations
        and if device does not support it them RuntimeError will be raised.

        :param address: i2c address of the target device
        :param register: address of the register to read
        :param num_bytes: number of bytes to read; this should match length of the register
        :param use_restart: True or False (default) indicating if we should try using I2C restart op between read and
                write operations
        :return: None if at any point during these transactions client sends NACK or actual Bits holding response data
        """

    def write_register(self, address: int, register: int, data: Bits | str | int, num_bytes: int = 1) -> bool:
        """
        Writes register to the target device. This is basically same as `write(...)` where first write byte is register
        address and subsequent bytes are values to write into a register.

        :param address: i2c address of the target device
        :param register: address of the register to write to
        :param data: array of bits to send to the target device.
        :param num_bytes: number of bytes to send or if None, then send all bits in `data` padded with zero bits.
        :return:
        """
        payload_length_bits = num_bytes * 8
        payload = BitArray(f"uint:{payload_length_bits}={data}") if isinstance(data, int) else BitArray(data)
        payload = payload[-payload_length_bits:] if payload.len > payload_length_bits else payload
        if payload.len < payload_length_bits:
            payload.prepend(BitArray(payload_length_bits - payload.len))

        return self.write(address, BitArray(f"uint:8={register}") + payload, num_bytes + 1)

    @abstractmethod
    def scan(self) -> list[int]:
        """
        Scans for all client devices connected on this I2C bus.

        :return: list of addresses of connected devices
        """
