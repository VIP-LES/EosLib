import struct

from typing_extensions import Self

from EosLib.format.base_format import BaseFormat

from EosLib.format.definitions import Type


class EmptyFormat(BaseFormat):

    def __init__(self, num_bytes=0):
        self.num_bytes = num_bytes

    def __eq__(self, other):
        return self.num_bytes == other.num_bytes

    @staticmethod
    def get_format_type() -> Type:
        return Type.EMPTY

    def encode(self) -> bytes:
        return struct.pack(self.get_format_string())

    @classmethod
    def decode(cls, data: bytes) -> Self:
        return EmptyFormat(len(data))

    def get_format_string(self) -> str:
        return self.num_bytes * "x"
