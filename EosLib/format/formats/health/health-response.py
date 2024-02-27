import struct

from typing_extensions import Self

from EosLib.device import Device
from EosLib.format.definitions import Type
from EosLib.format.base_format import BaseFormat


class HealthResponse(BaseFormat):
    @staticmethod
    def get_format_type() -> Type:
        return Type.HEALTH_RESPONSE

    @staticmethod
    def get_format_string() -> str:
        # Struct format is: device_id, response_type, num_entries, entries[]
        return "!" \
               "B" \
               "B" \
               "B" \
               "s"

    def __init__(self, device_id: Device, response_type: int, num_entries: int, entries: list[str]):
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
        if self.device_id < 0 or self.device_id >= len(Device):
            return False
        elif self.num_entries != len(self.entries):
            return False
        else:
            return True

    def encode(self) -> bytes:
        return struct.pack(self.get_format_string(),
                           self.device_id,
                           self.response_type,
                           self.num_entries,
                           self.entries)

    @classmethod
    def decode(cls, data: bytes) -> Self:
        unpacked_data = struct.unpack(cls.get_format_string(), data)
        return HealthResponse(unpacked_data[0], unpacked_data[1], unpacked_data[2], unpacked_data[3])

    def to_terminal_output_string(self) -> str:
        return f"{self.device_id} has {self.num_entries} entries"  # not sure what the output should be or if necessary
