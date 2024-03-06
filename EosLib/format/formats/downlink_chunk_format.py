import struct

from typing_extensions import Self

from EosLib.packet import Packet
from EosLib.format.definitions import Type
from EosLib.format.base_format import BaseFormat


class DownlinkChunkFormat(BaseFormat):
    chunk_header_format_string = "!" \
                                "I"

    def __init__(self, chunk_num: int, chunk_body: bytes):
        self.chunk_num = chunk_num
        self.chunk_body = chunk_body

    def __eq__(self, other):
        return self.chunk_num == other.chunk_num and self.chunk_body == other.chunk_body

    def _i_promise_all_abstract_methods_are_implemented(self) -> bool:
        return True

    @staticmethod
    def get_format_type() -> Type:
        return Type.DOWNLINK_CHUNK

    def encode(self) -> bytes:
        encoded_bytes = struct.pack(DownlinkChunkFormat.chunk_header_format_string, self.chunk_num)
        encoded_bytes += self.chunk_body
        return encoded_bytes

    @classmethod
    def decode(cls, data: bytes) -> Self:
        data_body = data[struct.calcsize(DownlinkChunkFormat.chunk_header_format_string):]
        chunk_num = struct.unpack(DownlinkChunkFormat.chunk_header_format_string,
                                  data[0:struct.calcsize(DownlinkChunkFormat.chunk_header_format_string)])[0]

        return DownlinkChunkFormat(chunk_num, data_body)

    def get_validity(self) -> bool:
        if self.chunk_num < 0 or self.chunk_body is None:
            return False
        else:
            return True
