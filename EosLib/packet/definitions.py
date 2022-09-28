from enum import IntEnum, unique


@unique
class PacketType(IntEnum):
    TELEMETRY = 0,
    WARNING = 1,
    ERROR = 2


@unique
class Priority(IntEnum):
    NO_TRANSMIT = 255,
    URGENT = 1,
    TELEMETRY = 2,
    DATA = 10


@unique
class Device(IntEnum):
    ALTIMETER = 1,
    GPS = 2,


@unique
class HeaderPreamble(IntEnum):
    DATA = 0,
    TRANSMIT = 1


class PacketFormatError(Exception):
    pass
