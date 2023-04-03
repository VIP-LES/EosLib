from dataclasses import dataclass
from enum import IntEnum, unique

from EosLib.device import Device


@unique
class ThreadStatus(IntEnum):
    UNHEALTHY = -1
    DISABLED = 0
    HEALTHY = 1


@dataclass
class DriverHealth:

    device_id: Device
    thread_count: int
    read_thread_status: int
    command_thread_status: int

    # Struct format is: device id, thread count, read thread status, command thread status
    struct_format_string: str = "!" \
                                "B" \
                                "B" \
                                "B" \
                                "B"
