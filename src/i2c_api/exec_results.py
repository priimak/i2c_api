from typing import NamedTuple

from bitstring import BitArray


class ExecResults(NamedTuple):
    data: list[list[BitArray]]
    is_success: bool

