import datetime
import math
import struct

from EosLib.packet import definitions
from EosLib.packet.definitions import PacketFormatError


class TransmitHeader:
    def __init__(self, send_seq_num: int, send_time: datetime.datetime = datetime.datetime.now()):
        self.send_seq_num = send_seq_num
        self.send_time = send_time

    def __eq__(self, other):
        return (self.send_seq_num == other.send_seq_num and
                math.isclose(self.send_time.timestamp(), other.send_time.timestamp()))

    # TODO: Expand validation criteria
    def validate_transmit_header(self):
        if self.send_time is None or self.send_seq_num is None:
            raise PacketFormatError("Transmit header has invalid value")
        return True

    def encode(self):
        self.validate_transmit_header()
        return struct.pack(definitions.transmit_header_struct_format_string, definitions.transmit_header_preamble,
                           self.send_seq_num, self.send_time.timestamp())


class DataHeader:
    def __init__(self, data_packet_generate_time: datetime.datetime = datetime.datetime.now(),
                 data_packet_type: definitions.PacketType = None, data_packet_sender: definitions.Device = None,
                 data_packet_priority: definitions.Priority = None,
                 ):
        self.data_packet_sender = data_packet_sender
        self.data_packet_type = data_packet_type
        self.data_packet_priority = data_packet_priority
        self.data_packet_generate_time = data_packet_generate_time

    def __eq__(self, other):
        return (self.data_packet_priority == other.data_packet_priority and
                self.data_packet_type == other.data_packet_type and
                self.data_packet_sender == other.data_packet_sender and
                math.isclose(self.data_packet_generate_time.timestamp(), other.data_packet_generate_time.timestamp()))

    # TODO: Expand validation criteria
    def validate_data_header(self):
        if (self.data_packet_sender is None or self.data_packet_type is None or
                self.data_packet_priority is None or self.data_packet_generate_time is None):
            raise PacketFormatError("Data header has invalid value")
        return True

    def encode(self):
        self.validate_data_header()
        return struct.pack(definitions.data_header_struct_format_string, definitions.data_header_preamble,
                           self.data_packet_generate_time.timestamp(), self.data_packet_type, self.data_packet_sender,
                           self.data_packet_priority)


class Packet:
    def __init__(self, body: bytes = None, data_header: DataHeader = None, transmit_header: TransmitHeader = None):
        self.body = body
        self.data_header = data_header
        self.transmit_header = transmit_header

    def __eq__(self, other):
        return (self.data_header == other.data_header and
                self.transmit_header == other.transmit_header and
                self.body == other.body)

    def encode_packet(self) -> bytes:
        """Validates and then returns the byte string version of the initialized packet.

        :return: Validated packet byte string
        """
        packet_bytes = b''
        if self.transmit_header is not None:
            packet_bytes += self.transmit_header.encode()

        packet_bytes += self.data_header.encode()
        packet_bytes += self.body

        return packet_bytes


def decode_transmit_header(header_bytes: bytes):
    if header_bytes[0] != definitions.transmit_header_preamble:
        raise PacketFormatError("Not a valid transmit header")

    unpacked = struct.unpack(definitions.transmit_header_struct_format_string, header_bytes)
    decoded_header = TransmitHeader(unpacked[1], datetime.datetime.fromtimestamp(unpacked[2]))
    return decoded_header


def decode_data_header(header_bytes: bytes):
    if header_bytes[0] != definitions.data_header_preamble:
        raise PacketFormatError("Not a valid data header")

    unpacked = struct.unpack(definitions.data_header_struct_format_string, header_bytes)
    decoded_header = DataHeader(datetime.datetime.fromtimestamp(unpacked[1]), unpacked[2], unpacked[3], unpacked[4])
    return decoded_header


def decode_packet(packet_bytes: bytes) -> Packet:
    """Takes a bytes object and decodes it into a Packet object.

    :param packet_bytes: The bytes object to be decoded
    :return: The decoded Packet object
    """
    decoded_packet = Packet()
    if packet_bytes[0] == definitions.transmit_header_preamble:
        decoded_transmit_header = decode_transmit_header(
            packet_bytes[0:struct.calcsize(definitions.transmit_header_struct_format_string)])
        decoded_packet.transmit_header = decoded_transmit_header
        packet_bytes = packet_bytes[struct.calcsize(definitions.transmit_header_struct_format_string):]

    if packet_bytes[0] == definitions.data_header_preamble:
        decoded_data_header = decode_data_header(
            packet_bytes[0:struct.calcsize(definitions.data_header_struct_format_string)])
        decoded_packet.data_header = decoded_data_header
        packet_bytes = packet_bytes[struct.calcsize(definitions.data_header_struct_format_string):]

    decoded_packet.body = packet_bytes

    return decoded_packet
