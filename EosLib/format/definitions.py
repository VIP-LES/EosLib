from enum import unique, IntEnum


class Type(IntEnum):
    NO_TYPE = 0
    TELEMETRY = 1
    WARNING = 2
    DATA = 3
    POSITION = 4
    TELEMETRY_DATA = 5
    EMPTY = 6
    RESPONSE_START = 32
    RESPONSE_1 = 33
    RESPONSE_2 = 34
    RESPONSE_3 = 35
    RESPONSE_4 = 36
    RESPONSE_END = 37
    COMMAND_START = 32
    COMMAND_1 = 40
    COMMAND_2 = 41
    COMMAND_3 = 42
    COMMAND_4 = 43
    COMMAND_END = 44
    ERROR = 255
