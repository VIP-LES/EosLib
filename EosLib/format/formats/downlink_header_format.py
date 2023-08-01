import csv
import io
import struct
from enum import IntEnum, unique

from typing_extensions import Self

from EosLib.format.definitions import Type
from EosLib.format.csv_format import CsvFormat


@unique
class DownlinkCommand(IntEnum):
    NO_COMMAND = 0
    START_REQUEST = 1
    START_ACKNOWLEDGEMENT = 2
    STOP_TRANSMISSION = 3
    ALL_CHUNKS_RECEIVED = 4


class DownlinkCommandFormat(CsvFormat):
    # Format contains: File ID, File Size (In number of chunks), command type
    format_string = "!" \
                    "H" \
                    "I" \
                    "B"

    def __init__(self, file_id: int, num_chunks: int, command_type: DownlinkCommand):
        self.file_id = file_id
        self.num_chunks = num_chunks
        self.command_type = command_type

    def __eq__(self, other):
        return self.file_id == other.file_id and\
            self.num_chunks == other.num_chunks and\
            self.command_type == other.command_type

    def get_csv_headers(self):
        return ["file_id", "num_chunks", "command_type"]

    def encode_to_csv(self) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([self.file_id,
                         self.num_chunks,
                         self.command_type])

        return output.getvalue()

    @classmethod
    def decode_from_csv(cls, csv_string: str) -> Self:
        reader = csv.reader([csv_string])
        csv_list = list(reader)[0]

        return DownlinkCommandFormat(*csv_list)

    @staticmethod
    def get_format_type() -> Type:
        return Type.DOWNLINK_COMMAND

    def encode(self) -> bytes:
        return struct.pack(self.format_string, self.file_id, self.num_chunks, self.command_type)

    @classmethod
    def decode(cls, data: bytes) -> Self:
        unpacked_data = struct.unpack(DownlinkCommandFormat.format_string, data)

        return DownlinkCommandFormat(*unpacked_data)
