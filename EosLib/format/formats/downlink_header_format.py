import csv
import io
import struct

from typing_extensions import Self

from EosLib.format import Type
from EosLib.format.csv_format import CsvFormat


class DownlinkHeaderFormat(CsvFormat):
    # Format contains: File ID, File Size (In number of chunks), is acknowledgement,
    format_string = "!" \
                    "H" \
                    "I" \
                    "?"

    def __init__(self, file_id: int, num_chunks: int, is_ack: bool = False):
        self.file_id = file_id
        self.num_chunks = num_chunks
        self.is_ack = is_ack

    def __eq__(self, other):
        return self.file_id == other.file_id and self.num_chunks == other.num_chunks and self.is_ack == other.is_ack

    def get_csv_headers(self):
        return ["file_id", "num_chunks", "is_ack"]

    def encode_to_csv(self) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([self.file_id,
                         self.num_chunks,
                         self.is_ack])

        return output.getvalue()

    @classmethod
    def decode_from_csv(cls, csv_string: str) -> Self:
        reader = csv.reader([csv_string])
        csv_list = list(reader)[0]

        return DownlinkHeaderFormat(*csv_list)

    @staticmethod
    def get_format_type() -> Type:
        return Type.DOWNLINK_HEADER

    def encode(self) -> bytes:
        return struct.pack(self.format_string, self.file_id, self.num_chunks, self.is_ack)

    @classmethod
    def decode(cls, data: bytes) -> Self:
        unpacked_data = struct.unpack(DownlinkHeaderFormat.format_string, data)

        return DownlinkHeaderFormat(*unpacked_data)
