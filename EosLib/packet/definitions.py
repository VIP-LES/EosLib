from enum import IntEnum, unique

RADIO_MAX_BYTES = 255


@unique
class PacketType(IntEnum):
    TELEMETRY = 0,
    WARNING = 1,
    ERROR = 2


@unique
class PacketPriority(IntEnum):
    NO_TRANSMIT = 255,
    URGENT = 1,
    TELEMETRY = 2,
    DATA = 10


@unique
class PacketDevice(IntEnum):
    ALTIMETER = 1,
    GPS = 2,


@unique
class HeaderPreamble(IntEnum):
    DATA = 2,
    TRANSMIT = 1
