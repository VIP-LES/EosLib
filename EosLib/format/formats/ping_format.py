import struct
from typing_extensions import Self
from EosLib.format.definitions import Type
from EosLib.format.base_format import BaseFormat

from enum import Flag


class PingEnum(Flag):
    PING = True
    ACK = False


class Ping(BaseFormat):
    @staticmethod
    def get_format_type() -> Type:
        return Type.PING

    @staticmethod
    def get_format_string() -> str:
        # Struct format is: ack
        return "!" \
               "?" \
               "B"

    def __init__(self, ping: PingEnum, num: int):
        self.ping = ping
        self.num = num
        self.valid = self.get_validity()

    def __eq__(self, other):
        return self.ping == other.ping and \
               self.num == other.num and \
               self.valid == other.valid

    def get_validity(self):
        if self.num < 0 or self.num > 255:
            return False
        else:
            return True

    def encode(self) -> bytes:
        return struct.pack(self.get_format_string(),
                           self.ping, self.num)

    @classmethod
    def decode(cls, data: bytes) -> Self:
        unpacked_data = struct.unpack(cls.get_format_string(), data)
        return Ping(unpacked_data[0], unpacked_data[1])

    def to_terminal_output_string(self) -> str:
        if self.ping:
            return "Received Ping: " + str(self.num)
        elif not self.ping:
            return "Received ACK: " + str(self.num)
