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


struct_format_string = "!" \
                       "d" \
                       "B" \
                       "d" \
                       "B" \
                       "B" \
                       "B"


class PacketFormatError(Exception):
    pass
