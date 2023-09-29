import struct
from typing_extensions import Self
from EosLib.format.definitions import Type


class CutDown:
    @staticmethod
    def get_format_type() -> Type:
        return Type.COMMAND

    @staticmethod
    def get_format_string() -> str:
        # Struct format is: ack
        return "!" \
               "B"

    def __init__(self, ack: int):
        self.ack = ack
        self.valid = self.get_validity()

    def __eq__(self, other):
        return self.ack == other.ack and \
               self.valid == other.valid

    def get_validity(self):
        if self.ack < 0 or self.ack > 255:
            return False
        else:
            return True

    def encode(self) -> bytes:
        return struct.pack(self.get_format_string(),
                           self.ack)

    @classmethod
    def decode(cls, data: bytes) -> Self:
        unpacked_data = struct.unpack(cls.get_format_string(), data)
        return CutDown(unpacked_data[0])
