import struct

from typing_extensions import Self

from EosLib.packet import Packet
from EosLib.format.definitions import Type
from EosLib.format.base_format import BaseFormat


class DownlinkChunkListFormat(BaseFormat):
    chunk_list_header_format_string = "!" \
                                      "B"

    def __init__(self, chunk_list: list[int]):
        self.chunk_list = chunk_list

    def __eq__(self, other):
        return self.chunk_list == other.chunk_list

    @staticmethod
    def get_format_type() -> Type:
        return Type.DOWNLINK_CHUNK_LIST

    @staticmethod
    def get_max_chunks():
        return Packet.radio_body_max_bytes - struct.calcsize(DownlinkChunkListFormat.chunk_list_header_format_string)

    def encode(self) -> bytes:
        if len(self.chunk_list) > DownlinkChunkListFormat.get_max_chunks():
            raise ValueError("Chunk list is too long")

        return struct.pack(DownlinkChunkListFormat.chunk_list_header_format_string,
                           len(self.chunk_list),
                           *self.chunk_list)

    @classmethod
    def decode(cls, data: bytes) -> Self:
        chunk_list_size = int(data[0])
        chunk_list = data[1:]

        decoded_list = list(struct.unpack(chunk_list_size*"I", chunk_list))
        return DownlinkChunkListFormat(decoded_list)
