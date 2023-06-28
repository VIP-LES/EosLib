from pathlib import Path

from EosLib.format.formats.downlink_header_format import DownlinkHeaderFormat
from EosLib.format.formats.downlink_chunk_format import DownlinkChunkFormat


class DownlinkReceiver:
    def __init__(self, downlink_header: DownlinkHeaderFormat, destination_path: str = None):
        if destination_path is None:
            self.destination_path = Path(".")

        self.file_id = downlink_header.file_id
        self.num_chunks = downlink_header.num_chunks

    def get_ack(self) -> DownlinkHeaderFormat:
        return DownlinkHeaderFormat(self.file_id, self.num_chunks, True)
