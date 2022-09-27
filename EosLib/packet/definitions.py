from enum import Enum, IntEnum, unique


@unique
class PacketType(Enum):
    TELEMETRY = 0,
    WARNING = 1,
    ERROR = 2


@unique
class Priority(IntEnum):
    NO_TRANSMIT = -1,
    URGENT = 1,
    TELEMETRY = 2,
    DATA = 10


@unique
class Device(Enum):
    ALTIMETER = 1,
    GPS = 2,


struct_format_string = "!" \
                       "d" \
                       "c" \
                       "9x" \
                       "" \
                       "d" \
                       "c" \
                       "c" \
                       "c" \
                       "7x"

if __name__ == "__main__":
    print(struct_format_string)
