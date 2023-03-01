import struct
from datetime import datetime

from EosLib import Type
from EosLib.packet.packet import Packet

class Telemetry:
    #Struct format is: timestamp, temperature, pressure, humidity, roll-x, pitch-y, yaw-z
    telemetry_struct_string = "!" \
                              "d" \
                              "d" \
                              "d" \
                              "d" \
                              "d" \
                              "d"
    

    def __init__(self, timestamp: float = 0.0, temperature: float = 0.0, pressure: float = 0.0, humidity: float = 0.0, rollX: float = 0.0, pitchY: float = 0.0, yawZ: float = 0.0):
        self.timestamp = timestamp
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.rollX = rollX
        self.pitchY = pitchY
        self.yawZ = yawZ
        self.valid = False

    def set_validity(self):
        if (self.pressure < 0 or self.humidity < 0 or self.humidity > 100):
            self.valid = False
        else:
            self.valid = True

    @staticmethod
    def decode_data(data_packet: Packet):
        newData = Telemetry()
        newData.data_packet = data_packet
        if (newData.data_packet.data_header.data_type != Type.DATA):
            raise ValueError("Packet is not data")
        
        unpacked_tuple = struct.unpack(Telemetry.telemetry_struct_string, newData.data_packet.body)
        newData.timestamp = unpacked_tuple[0]
        newData.temperature = unpacked_tuple[1]
        newData.pressure = unpacked_tuple[2]
        newData.humidity = unpacked_tuple[3]
        newData.rollX = unpacked_tuple[4]
        newData.pitchY = unpacked_tuple[5]
        newData.yawZ = unpacked_tuple[6]
        newData.set_validity()

        return newData
    
    def encode_data(self) -> bytes:
        return struct.pack(Telemetry.telemetry_struct_string, self.timestamp, self.temperature, self.pressure, self.humidity, self.rollX, self.pitchY, self.yawZ)