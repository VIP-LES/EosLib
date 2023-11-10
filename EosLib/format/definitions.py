from enum import unique, IntEnum


@unique
class Type(IntEnum):
    NO_TYPE = 0
    TELEMETRY = 1
    WARNING = 2
    DATA = 3
    POSITION = 4
    COMMAND = 5
    RESPONSE = 6
    TELEMETRY_DATA = 7
    EMPTY = 8
    CUTDOWN = 9
    PING = 10
    VALVE = 11
    E_FIELD = 12
    ERROR = 255
