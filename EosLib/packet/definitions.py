from enum import Enum


class PacketType(Enum):
    TELEMETRY = 0,
    WARNING = 1,
    ERROR = 2


class Priority(Enum):
    NO_TRANSMIT = -1,
    URGENT = 1,
    TELEMETRY = 2,
    DATA = 10

