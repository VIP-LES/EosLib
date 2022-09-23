from enum import Enum, unique


@unique
class PacketType(Enum):
    TELEMETRY = 0,
    WARNING = 1,
    ERROR = 2


@unique
class Priority(Enum):
    NO_TRANSMIT = -1,
    URGENT = 1,
    TELEMETRY = 2,
    DATA = 10


@unique
class Device(Enum):
    ALTIMETER = 1,
    GPS = 2,
