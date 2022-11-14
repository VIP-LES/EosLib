import struct
from enum import IntEnum, unique


@unique
class Type(IntEnum):
    TELEMETRY = 0
    WARNING = 1
    DATA = 2
    ERROR = 255


@unique
class Priority(IntEnum):
    NO_TRANSMIT = 255
    URGENT = 1
    TELEMETRY = 2
    DATA = 10


@unique
class Device(IntEnum):
    TEMPERATURE_HUMIDITY = 0
    PRESSURE = 1
    PARTICULATES = 2
    IR_VISIBLE_LIGHT = 3
    VISIBLE_UVA_LIGHT = 4
    UVA_UVB_LIGHT = 5
    CO2 = 6
    O3 = 7
    MISC_SENSOR_1 = 8
    MISC_SENSOR_2 = 9
    MISC_SENSOR_3 = 10
    MISC_SENSOR_4 = 11
    REEFING_MOTOR = 12
    MISC_ENGINEERING_1 = 13
    MISC_ENGINEERING_2 = 14
    CAMERA_1 = 15
    CAMERA_2 = 16
    MISC_CAMERA_1 = 17
    MISC_CAMERA_2 = 18
    RADIO = 19
    MISC_RADIO_1 = 20
    MISC_RADIO_2 = 21
    GPS = 22
    IMU = 23
    MISC_1 = 24
    MISC_2 = 25
    MISC_3 = 26
    MISC_4 = 27


@unique
class HeaderPreamble(IntEnum):
    V010DATA = 2,
    TRANSMIT = 1,
    DATA = 3


old_data_headers = [HeaderPreamble.V010DATA]
old_transmit_headers = []
