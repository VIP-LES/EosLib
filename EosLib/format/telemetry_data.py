import struct
from datetime import datetime
from EosLib import Type
from EosLib.packet.packet import Packet


class TelemetryData:
    # Struct format is: timestamp, temperature, pressure, humidity, roll-x, pitch-y, yaw-z
    telemetry_struct_string = "!" \
                              "d" \
                              "d" \
                              "d" \
                              "d" \
                              "d" \
                              "d" \
                              "d"

    # Initialize data to params (default values otherwise)
    """Initializes data to parameters (default values otherwise)

    :param self: Itself
    :type self: TelemetryData
    :param timestamp: The time and date of data collected
    :type timestamp: DATETYPE
    :param temperature: The temperature data
    :type temperature: float
    :param pressure: The pressure data
    :type pressure: float
    :param humidity: The humidity data
    :type humidity: float
    :param x_rotation: The x rotation data
    :param y_rotation: The y rotation data
    :param z_rotation: The z rotation data
    """
    def __init__(self, timestamp: float = datetime.now(), temperature: float = float("NaN"), pressure: float = float("NaN"), humidity: float = float("NaN"),
                 x_rotation: float = float("NaN"), y_rotation: float = float("NaN"), z_rotation: float = float("NaN")):
        self.timestamp = timestamp
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.x_rotation = x_rotation
        self.y_rotation = y_rotation
        self.z_rotation = z_rotation
        self.valid = False

    """Checks if data is valid (NEED A MORE CONTRETE WAY OF VALIDATING)
    
    :param self: Itself;
    :type self: TelemetryData
    """
    def set_validity(self):
        if self.pressure < 0 or self.humidity < 0 or self.humidity > 100:
            self.valid = False
        else:
            self.valid = True

    """Stores data from packet into respective variables

    :param data_packet: The data packet received from sensor to decode
    :type data_packet: Packet
    :returns: Object with decoded data
    :rtype: TelemetryData
    """
    @staticmethod
    def decode_data(data_packet: Packet) -> "TelemetryData":
        new_data = TelemetryData()
        if data_packet.data_header.data_type != Type.T_DATA:
            raise ValueError("Packet is not data")

        unpacked_tuple = struct.unpack(TelemetryData.telemetry_struct_string, data_packet.body)
        new_data.timestamp = unpacked_tuple[0]
        new_data.temperature = unpacked_tuple[1]
        new_data.pressure = unpacked_tuple[2]
        new_data.humidity = unpacked_tuple[3]
        new_data.x_rotation = unpacked_tuple[4]
        new_data.y_rotation = unpacked_tuple[5]
        new_data.z_rotation = unpacked_tuple[6]
        new_data.set_validity()

        return new_data

    # Takes data and sends it as a byte
    """Takes data and sends it as a byte

    :param self: Itself
    :type self: TelemetryData
    :returns: Struct with encoded data
    :rtype: bytes
    """
    def encode(self) -> bytes:
        return struct.pack(TelemetryData.telemetry_struct_string, self.timestamp, self.temperature, self.pressure,
                           self.humidity,
                           self.x_rotation, self.y_rotation, self.z_rotation)
