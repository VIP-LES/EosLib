import struct
from datetime import datetime
from EosLib import Type
from EosLib.packet.packet import Packet


class TelemetryData:
    # Struct format is: timestamp, temperature, pressure, humidity, x_rotation, y_rotation, z_rotation
    telemetry_struct_string = "!" \
                              "d" \
                              "d" \
                              "d" \
                              "d" \
                              "d" \
                              "d" \
                              "d"

    def __init__(self, timestamp: datetime = None, temperature: float = None,
                 pressure: float = None, humidity: float = None,
                 x_rotation: float = None, y_rotation: float = None, z_rotation: float = None):
        """Initializes data to parameters (default values otherwise)

        :param timestamp: The time and date of data collected
        :param temperature: The temperature data
        :param pressure: The pressure data
        :param humidity: The humidity data
        :param x_rotation: The x rotation data
        :param y_rotation: The y rotation data
        :param z_rotation: The z rotation data
        """
        self.timestamp = datetime.now() if timestamp is None else timestamp
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.x_rotation = x_rotation
        self.y_rotation = y_rotation
        self.z_rotation = z_rotation
        self.valid = False

    def set_validity(self):
        """Checks if data is valid (NEED A MORE CONCRETE WAY OF VALIDATING)

        """
        if self.pressure < 0 or self.humidity < 0 or self.humidity > 100:
            self.valid = False
        else:
            self.valid = True

    @staticmethod
    def decode_data(data_packet: Packet | bytes) -> "TelemetryData":
        """Stores data from packet into respective variables

        :param data_packet: The data packet received from sensor to decode
        :returns: Object with decoded data
        """
        if isinstance(data_packet, Packet):
            if data_packet.data_header.data_type != Type.TELEMETRY_DATA:
                raise ValueError("Packet is not telemetry data")
            packet_body = data_packet.body
        else:
            packet_body = data_packet
        unpacked_tuple = struct.unpack(TelemetryData.telemetry_struct_string, packet_body)
        new_data = TelemetryData(datetime.fromtimestamp(unpacked_tuple[0]), unpacked_tuple[1], unpacked_tuple[2],
                                 unpacked_tuple[3], unpacked_tuple[4], unpacked_tuple[5], unpacked_tuple[6])
        new_data.set_validity()
        return new_data

    def encode(self) -> bytes:
        """Takes data and sends it as a byte

        :returns: Struct with encoded data
        """
        return struct.pack(TelemetryData.telemetry_struct_string, self.timestamp.timestamp(), self.temperature,
                           self.pressure,
                           self.humidity, self.x_rotation, self.y_rotation, self.z_rotation)
