import datetime
import struct
from enum import IntEnum
from typing_extensions import Self

import EosLib
from EosLib.format.csv_format import CsvFormat
from EosLib.packet import Packet


class FlightState(IntEnum):
    NOT_SET = 0
    UNKNOWN = 1
    ON_GROUND = 2
    ASCENT = 3
    DESCENT = 4


class Position(CsvFormat):
    # Struct format is: GPS timestamp, lat, long, speed, altitude, number of satellites, flight state
    gps_struct_string = "!" \
                        "d" \
                        "d" \
                        "d" \
                        "d" \
                        "d" \
                        "H" \
                        "B"

    def __init__(self,
                 gps_time: datetime.datetime.now(),
                 latitude: float,
                 longitude: float,
                 speed: float,
                 altitude: float,
                 number_of_satellites: int,
                 flight_state: FlightState = FlightState.NOT_SET):
        self.gps_time = gps_time
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.speed = speed
        self.number_of_satellites = number_of_satellites
        self.flight_state = flight_state

        self.valid = self.get_validity()

    def encode(self) -> bytes:
        return struct.pack(self.gps_struct_string,
                           self.gps_time.timestamp(),
                           self.latitude,
                           self.longitude,
                           self.speed,
                           self.altitude,
                           self.number_of_satellites,
                           self.flight_state)

    @classmethod
    def decode(cls, data: bytes | Packet) -> Self:
        if isinstance(data, Packet):
            if data.data_header.data_type != EosLib.Type.POSITION:
                raise ValueError("Attempted to decode a non-position packet using Position")
            else:
                data = data.body

        unpacked_data = struct.unpack(cls.gps_struct_string, data)

        return Position(datetime.datetime.fromtimestamp(unpacked_data[0]),
                        unpacked_data[1],
                        unpacked_data[2],
                        unpacked_data[3],
                        unpacked_data[4],
                        unpacked_data[5],
                        FlightState(unpacked_data[6]))

    def get_csv_headers(self):
        return ["GPS Timestamp", "Latitude", "Longitude", "Speed", "Altitude", "Number of Satellites", "Flight State"]

    def encode_to_csv(self) -> str:
        return ",".join([self.gps_time.isoformat(),
                         str(self.latitude),
                         str(self.longitude),
                         str(self.speed),
                         str(self.altitude),
                         str(self.number_of_satellites),
                         str(self.flight_state.value)])

    @classmethod
    def decode_from_csv(cls, csv: str) -> Self:
        csv_list = csv.split(",")

        return Position(datetime.datetime.fromisoformat(csv_list[0]),
                        float(csv_list[1]),
                        float(csv_list[2]),
                        float(csv_list[3]),
                        float(csv_list[4]),
                        int(csv_list[5]),
                        FlightState(int(csv_list[6])))

    def get_validity(self):
        if (self.number_of_satellites < 4 or
                self.latitude == 0 or
                self.longitude == 0):
            return False
        else:
            return True
