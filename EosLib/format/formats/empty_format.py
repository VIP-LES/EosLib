import struct

from typing_extensions import Self

from EosLib.format.base_format import BaseFormat

from EosLib.format.definitions import Type


class EmptyFormat(BaseFormat):
    """ This is an empty format class, primarily used for testing purposes. It only has one property, size, which
    controls how many empty bytes are included in the format class.
    """

    def __init__(self, num_bytes=0):
        if num_bytes < 0:
            raise ValueError("num_bytes must be equal to or greater than 0")
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

    def get_validity(self) -> bool:
        return self.num_bytes >= 0
