import pytest
from bitstring import BitArray, Bits

from src.i2c_api import I2CMaster


def test_mk_payload_int():
    # single int as argument creates BitArray of one byte length and valid values for int are from 0 to 255 inclusive.
    assert I2CMaster.mk_payload(0) == BitArray("uint:8=0")
    assert I2CMaster.mk_payload(7) == BitArray("uint:8=7")
    assert I2CMaster.mk_payload(255) == BitArray("uint:8=255")

    with pytest.raises(ValueError):
        I2CMaster.mk_payload(300)

    with pytest.raises(ValueError):
        I2CMaster.mk_payload(-1)


def test_mk_payload_list():
    assert I2CMaster.mk_payload([7]) == BitArray("uint:8=7")
    payload = I2CMaster.mk_payload([7, 10])
    assert payload == BitArray("uint:16=1802")

    with pytest.raises(ValueError):
        I2CMaster.mk_payload([700, 2])


def test_mk_payload_str():
    assert I2CMaster.mk_payload("0b00000010") == BitArray("uint:8=2")


def test_mk_payload_bits():
    assert I2CMaster.mk_payload(Bits("0x02")) == BitArray("uint:8=2")


def test_pad():
    data = BitArray("uint:7=3")
    assert data.len == 7

    # 7 bit array should be auto-padded to 8 bits
    padded_data = I2CMaster.pad_payload(data)
    assert padded_data.len == 8

    # 10 bit array should be auto-padded to 16 bits (2 bytes)
    padded_data = I2CMaster.pad_payload(BitArray("0b1111111111"))
    assert padded_data.len == 16
    assert padded_data == BitArray("0b0000001111111111")

    # if num bytes to be padded to is provided then data will be padded to the requested length

    padded_data = I2CMaster.pad_payload(data, 3)
    assert padded_data.len == 24
