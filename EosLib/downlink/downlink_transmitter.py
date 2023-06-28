import math
import os
import queue

from typing import BinaryIO

from EosLib.format.formats.downlink_header_format import DownlinkHeaderFormat
from EosLib.format.formats.downlink_chunk_format import DownlinkChunkFormat


class DownlinkTransmitter:
    def __init__(self, downlink_file: BinaryIO, file_id: int):
        self.downlink_file = downlink_file

        self.file_id = file_id

        self.downlink_file.seek(0, os.SEEK_END)
        self.downlink_file_size = downlink_file.tell()
        self.downlink_file.seek(0)

        self.num_chunks = int(math.ceil(self.downlink_file_size / DownlinkChunkFormat.get_chunk_size()))

        self.chunk_queue = queue.SimpleQueue()

        self.is_acknowledged = False

    def get_downlink_header(self) -> DownlinkHeaderFormat:
        return DownlinkHeaderFormat(self.file_id, self.num_chunks)

    def get_chunk(self, chunk_num: int) -> DownlinkChunkFormat:
        self.downlink_file.seek(chunk_num * DownlinkChunkFormat.get_chunk_size())
        chunk_body = self.downlink_file.read(DownlinkChunkFormat.get_chunk_size())
        return DownlinkChunkFormat(chunk_num, chunk_body)

    def get_next_chunk(self) -> DownlinkChunkFormat | None:
        if self.chunk_queue.empty():
            return None

        return self.get_chunk(self.chunk_queue.get())

    def add_ack(self, ack: DownlinkHeaderFormat) -> bool:
        if ack.file_id == self.file_id and ack.num_chunks == self.num_chunks and ack.is_ack:
            self.is_acknowledged = True
            return True
        else:
            return False
