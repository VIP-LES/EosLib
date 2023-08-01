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
    DOWNLINK_COMMAND = 9
    DOWNLINK_CHUNK = 10
    DOWNLINK_CHUNK_LIST = 11
    ERROR = 255
