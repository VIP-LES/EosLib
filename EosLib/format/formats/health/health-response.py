import struct
from enum import unique, IntEnum

from typing_extensions import Self

from EosLib.device import Device
from EosLib.format.definitions import Type
from EosLib.format.base_format import BaseFormat


@unique
class ResponseType(IntEnum):
    DEVICE = 0
    HISTORY = 1


class HealthResponse(BaseFormat):
    @staticmethod
    def get_format_type() -> Type:
        return Type.HEALTH_RESPONSE

    @staticmethod
    def get_format_string(self) -> str:
        # Struct format is: device_id, response_type, num_entries, entries[]
        return "!" \
               "B" \
               "B" \
               "B" \
               "Bd"*len(self.entries)

    def __init__(self, device_id: Device, response_type: ResponseType, num_entries: int, entries: list[tuple[int, float]]):
        self.device_id = device_id
        self.response_type = response_type
        self.num_entries = num_entries
        self.entries = entries
        self.valid = self.get_validity()

    def __eq__(self, other):
        return self.device_id == other.device_id and \
               self.response_type == other.response_type and \
               self.num_entries == other.num_entries and \
               self.entries == other.entries and \
               self.valid == other.get_validity()

    def get_validity(self) -> bool:
        all_valid = True
        if self.device_id < 0 or self.device_id >= len(Device):
            all_valid = False
        elif self.num_entries != len(self.entries):
            all_valid = False
        try:
            ResponseType(self.response_type)
        except ValueError:
            all_valid = False
        return all_valid

    def encode(self) -> bytes:
        return struct.pack(self.get_format_string(),
                           self.device_id,
                           self.response_type,
                           self.num_entries,
                           *self.entries)

    @classmethod
    def decode(cls, data: bytes) -> Self:
        constant_part_format_string = "!BBB"
        offset = struct.calcsize(constant_part_format_string)
        device_id, response_type, num_entries = struct.unpack(constant_part_format_string, data[:offset])

        entries_format_string = "Bd"*num_entries
        entries_as_tuple = struct.unpack(entries_format_string, data[offset:])
        entries = [(entries_as_tuple[i], entries_as_tuple[i + 1]) for i in range(0, len(entries_as_tuple), 2)]
        return HealthResponse(device_id, response_type, num_entries, entries)

    def to_terminal_output_string(self) -> str:
        return f"{self.device_id} has {self.num_entries} entries"  # not sure what the output should be or if necessary
