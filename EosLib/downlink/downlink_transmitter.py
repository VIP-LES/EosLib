from __future__ import annotations

import math
import os
import queue
import random

from typing import BinaryIO

from EosLib.format.formats.downlink_header_format import DownlinkCommandFormat, DownlinkCommand
from EosLib.format.formats.downlink_chunk_format import DownlinkChunkFormat


class DownlinkTransmitter:
    def __init__(self, downlink_file: BinaryIO, file_id: int):
        self.downlink_file = downlink_file

        self.file_id = file_id
    # find size of file
        self.downlink_file.seek(0, os.SEEK_END)
        self.downlink_file_size = downlink_file.tell()
        self.downlink_file.seek(0)
    # split the file into chunks based on max chunk file
        self.num_chunks = int(math.ceil(self.downlink_file_size / DownlinkChunkFormat.get_chunk_size()))
        self.chunk_queue = queue.SimpleQueue()

        self.is_acknowledged = False
    # add chunks to queue
        for i in range(0, self.num_chunks):
            self.chunk_queue.put(i)

    def get_downlink_header(self) -> DownlinkCommandFormat:
        return DownlinkCommandFormat(self.file_id, self.num_chunks, DownlinkCommand.START_REQUEST)

    def get_chunk(self, chunk_num: int) -> DownlinkChunkFormat:
        self.downlink_file.seek(chunk_num * DownlinkChunkFormat.get_chunk_size())
        chunk_body = self.downlink_file.read(DownlinkChunkFormat.get_chunk_size())
        return DownlinkChunkFormat(chunk_num, chunk_body)

    def get_next_chunk(self) -> DownlinkChunkFormat | None:
        if self.chunk_queue.empty():
            return None

        return self.get_chunk(self.chunk_queue.get())

    def add_ack(self, ack: DownlinkCommandFormat) -> bool:
        if ack.file_id == self.file_id and\
                ack.num_chunks == self.num_chunks and\
                ack.command_type == DownlinkCommand.START_ACKNOWLEDGEMENT:
            self.is_acknowledged = True
            return True
        else:
            return False
