import csv
import datetime
import io
import struct
from enum import IntEnum
from typing_extensions import Self

from EosLib.format.definitions import Type
from EosLib.format.csv_format import CsvFormat


class FlightState(IntEnum):
    NOT_SET = 0
    UNKNOWN = 1
    ON_GROUND = 2
    ASCENT = 3
    DESCENT = 4


class Position(CsvFormat):

    def __init__(self,
                 gps_time: datetime.datetime | None,
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

    def __eq__(self, other):
        return self.gps_time == other.gps_time and \
               self.latitude == other.latitude and \
               self.longitude == other.longitude and \
               self.speed == other.speed and \
               self.altitude == other.altitude and \
               self.number_of_satellites == other.number_of_satellites and \
               self.flight_state == other.flight_state

    @staticmethod
    def get_format_type() -> Type:
        return Type.POSITION

    @staticmethod
    def get_format_string() -> str:
        # Struct format is: GPS timestamp, lat, long, speed, altitude, number of satellites, flight state
        return "!" \
               "d" \
               "d" \
               "d" \
               "d" \
               "d" \
               "H" \
               "B"

    def encode(self) -> bytes:
        return struct.pack(self.get_format_string(),
                           self.gps_time.timestamp() if self.gps_time else 0,
                           self.latitude,
                           self.longitude,
                           self.speed,
                           self.altitude,
                           self.number_of_satellites,
                           self.flight_state)

    @classmethod
    def decode(cls, data: bytes) -> Self:
        unpacked_data = struct.unpack(cls.get_format_string(), data)

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
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([self.gps_time.isoformat() if self.gps_time else "None",
                         str(self.latitude),
                         str(self.longitude),
                         str(self.speed),
                         str(self.altitude),
                         str(self.number_of_satellites),
                         str(self.flight_state.value)])

        return output.getvalue()

    @classmethod
    def decode_from_csv(cls, csv_string: str) -> Self:
        reader = csv.reader([csv_string])
        csv_list = list(reader)[0]

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
