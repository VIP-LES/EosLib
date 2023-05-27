import struct
from typing_extensions import Self

import EosLib
from EosLib.packet.packet import Packet
from EosLib.format.csv_format import CsvFormat


class TelemetryData(CsvFormat):

    @staticmethod
    def get_format_type() -> EosLib.Type:
        return EosLib.Type.TELEMETRY_DATA

    # Struct format is: temperature, pressure, humidity, x_rotation, y_rotation, z_rotation
    telemetry_struct_string = "!" \
                              "d" \
                              "d" \
                              "d" \
                              "d" \
                              "d" \
                              "d"

    def __init__(self,
                 temperature: float = None,
                 pressure: float = None,
                 humidity: float = None,
                 x_rotation: float = None,
                 y_rotation: float = None,
                 z_rotation: float = None):
        """Initializes data to parameters (default values otherwise)

        :param temperature: The temperature data
        :param pressure: The pressure data
        :param humidity: The humidity data
        :param x_rotation: The x rotation data
        :param y_rotation: The y rotation data
        :param z_rotation: The z rotation data
        """
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.x_rotation = x_rotation
        self.y_rotation = y_rotation
        self.z_rotation = z_rotation
        self.valid = self.get_validity()



    def get_validity(self):
        """Checks if data is valid (NEED A MORE CONCRETE WAY OF VALIDATING)

        """
        if self.pressure < 0 or self.humidity < 0 or self.humidity > 100:
            return False
        else:
            return True

    def encode(self) -> bytes:
        return struct.pack(self.telemetry_struct_string,
                           self.temperature,
                           self.pressure,
                           self.humidity,
                           self.x_rotation,
                           self.y_rotation,
                           self.z_rotation)

    @classmethod
    def decode(cls, data: bytes | EosLib.packet.Packet) -> Self:
        if isinstance(data, Packet):
            if data.data_header.data_type != EosLib.Type.TELEMETRY_DATA:
                raise ValueError("Attempted to decode a non-telemetry_data packet using Position")
            else:
                data = data.body

        unpacked_data = struct.unpack(cls.telemetry_struct_string, data)

        return TelemetryData(unpacked_data[0],
                             unpacked_data[1],
                             unpacked_data[2],
                             unpacked_data[3],
                             unpacked_data[4],
                             unpacked_data[5])

    def get_csv_headers(self):
        return ["temperature", "pressure", "humidity", "x_rotation", "y_rotation", "z_rotation"]

    def encode_to_csv(self) -> str:
        return ",".join([str(self.temperature),
                         str(self.pressure),
                         str(self.humidity),
                         str(self.x_rotation),
                         str(self.y_rotation),
                         str(self.z_rotation)])

    @classmethod
    def decode_from_csv(cls, csv: str) -> Self:
        csv_list = csv.split(",")

        return TelemetryData(float(csv_list[0]),
                             float(csv_list[1]),
                             float(csv_list[2]),
                             float(csv_list[3]),
                             float(csv_list[4]),
                             float(csv_list[5]))
