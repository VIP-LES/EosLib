import io
from pathlib import Path
from typing import BinaryIO

from EosLib.format.formats.downlink_header_format import DownlinkCommandFormat, DownlinkCommand
from EosLib.format.formats.downlink_chunk_format import DownlinkChunkFormat
from EosLib.packet import Packet


class DownlinkReceiver:
    def __init__(self, downlink_header_packet: Packet,
                 downlink_header: DownlinkCommandFormat,
                 destination_dir: str = None):
        if destination_dir is None:
            self.destination_dir = Path(".")

        self.file_id = downlink_header.file_id
        self.num_chunks = downlink_header.num_chunks

        self.last_chunk_received = -1

        self.file_name = f"{downlink_header_packet.data_header.sender.name}-{downlink_header.file_id}.png"
        self.destination_path = self.destination_dir / self.file_name
        self.destination_file: BinaryIO = io.open(self.destination_path, "wb")

    def write_chunk(self, incoming_chunk: DownlinkChunkFormat):
        self.destination_file.seek(incoming_chunk.chunk_num*incoming_chunk.get_chunk_size())
        self.destination_file.write(incoming_chunk.chunk_body)

    def cleanup(self):
        pass

    def get_ack(self) -> DownlinkCommandFormat:
        return DownlinkCommandFormat(self.file_id, self.num_chunks, DownlinkCommand.START_ACKNOWLEDGEMENT)
