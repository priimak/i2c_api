from functools import reduce
from typing import NamedTuple

from bitstring import BitArray


class ExecResults(NamedTuple):
    data: list[list[BitArray]]
    is_success: bool

    def values(self) -> list[BitArray]:
        """Returns contained response data as a list of BitArray with consecutive bytes combined"""
        return [reduce(lambda v, acc: v + acc, [BitArray(f"uint:8={x}") for x in rsp], BitArray()) for rsp in self.data]

    def pp(self) -> str:
        """Pretty print"""
        values_ = ["0b" + v.bin for v in self.values()]
        return f"ExecResults(values={values_}, is_success={self.is_success})"
