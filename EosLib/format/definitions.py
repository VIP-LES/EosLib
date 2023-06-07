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
    ERROR = 255
