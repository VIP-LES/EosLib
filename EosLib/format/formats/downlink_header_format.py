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
    START_ACK = 2
    RETRANSMIT_MISSING_CHUNKS = 3
    STOP_TRANSMISSION = 4
    ERROR = 255


class DownlinkCommandFormat(CsvFormat):
    # Format contains: File ID, File Size (In number of chunks), command type, missing chunks (set of chunk nums)
    format_string = "!" \
                    "H" \
                    "I" \
                    "B"

    def __init__(self, file_id: int, num_chunks: int, command_type: DownlinkCommand, missing_chunks=None):
        self.file_id = file_id
        self.num_chunks = num_chunks
        self.command_type = command_type
        self.missing_chunks = missing_chunks
        if self.missing_chunks:
            self.format_string += 'i'*len(self.missing_chunks)
        self.valid = self.get_validity()

    def __eq__(self, other):
        return self.file_id == other.file_id and\
            self.num_chunks == other.num_chunks and\
            self.command_type == other.command_type and\
            self.missing_chunks == other.missing_chunks and\
            self.valid == other.valid

    def _i_promise_all_abstract_methods_are_implemented(self) -> bool:
        return True

    def get_csv_headers(self):
        return ["file_id", "num_chunks", "command_type", "missing_chunks"]

    def encode_to_csv(self) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([self.file_id,
                         self.num_chunks,
                         self.command_type,
                         self.missing_chunks])

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
        return struct.pack(self.format_string, self.file_id, self.num_chunks, self.command_type, *self.missing_chunks)

    @classmethod
    def decode(cls, data: bytes) -> Self:
        unpacked_data = struct.unpack(DownlinkCommandFormat.format_string, data)

        return DownlinkCommandFormat(*unpacked_data)

    def get_validity(self) -> bool:
        if self.num_chunks < 0:
            return False
        else:
            return True
