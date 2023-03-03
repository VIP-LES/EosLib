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
    def __init__(self, timestamp: float = 0, temperature: float = 0.0, pressure: float = 0.0, humidity: float = 0.0,
                 rollX: float = 0.0, pitchY: float = 0.0, yawZ: float = 0.0):
        self.timestamp = timestamp
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.rollX = rollX
        self.pitchY = pitchY
        self.yawZ = yawZ
        self.valid = False

    # Checks if data is valid (NEED A MORE CONCRETE WAY OF VALIDATING)
    def set_validity(self):
        if self.pressure < 0 or self.humidity < 0 or self.humidity > 100:
            self.valid = False
        else:
            self.valid = True

    # Stores data from packet into respective variables
    @staticmethod
    def decode_data(data_packet: Packet):
        new_data = TelemetryData()
        new_data.data_packet = data_packet
        if new_data.data_packet.data_header.data_type != Type.DATA:
            raise ValueError("Packet is not data")

        unpacked_tuple = struct.unpack(TelemetryData.telemetry_struct_string, new_data.data_packet.body)
        new_data.timestamp = unpacked_tuple[0]
        new_data.temperature = unpacked_tuple[1]
        new_data.pressure = unpacked_tuple[2]
        new_data.humidity = unpacked_tuple[3]
        new_data.rollX = unpacked_tuple[4]
        new_data.pitchY = unpacked_tuple[5]
        new_data.yawZ = unpacked_tuple[6]
        new_data.set_validity()

        return new_data

    # Takes data and sends it as a byte
    def encode_data(self) -> bytes:
        return struct.pack(TelemetryData.telemetry_struct_string, self.timestamp, self.temperature, self.pressure,
                           self.humidity,
                           self.rollX, self.pitchY, self.yawZ)
