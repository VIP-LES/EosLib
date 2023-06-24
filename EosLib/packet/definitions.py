from enum import IntEnum, unique


@unique
class Priority(IntEnum):
    NO_TRANSMIT = 0
    URGENT = 11
    TELEMETRY = 9
    DATA_HIGH = 7
    DATA = 5
    DATA_LOW = 3
    ERROR = 255


@unique
class HeaderPreamble(IntEnum):
    V010DATA = 2
    V020DATA = 3
    V030DATA = 4
    V201TRANSMIT = 6
    V020TRANSMIT = 1
    TRANSMIT = 7
    DATA = 5


old_data_headers = [HeaderPreamble.V010DATA, HeaderPreamble.V020DATA, HeaderPreamble.V030DATA]
old_transmit_headers = [HeaderPreamble.V020TRANSMIT, HeaderPreamble.V201TRANSMIT]
