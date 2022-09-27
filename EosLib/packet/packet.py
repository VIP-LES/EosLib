import datetime
import struct

from EosLib.packet import definitions
from EosLib.packet.definitions import PacketFormatError


class Packet:
    def __init__(self, send_time: datetime.datetime = None, send_seq_num: int = None,
                 data_generate_time: datetime.datetime = None, data_packet_type: definitions.PacketType = None,
                 data_packet_sender: definitions.Device = None, data_packet_priority: definitions.Priority = None,
                 body=None, is_radio: bool = False):
        self.send_time = send_time
        self.send_seq_num = send_seq_num
        self.data_generate_time = data_generate_time
        self.data_packet_type = data_packet_type
        self.data_packet_sender = data_packet_sender
        self.data_packet_priority = data_packet_priority
        self.body = body
        self.is_radio = is_radio

    def __eq__(self, other):
        return (self.send_time == other.send_time and
                self.send_seq_num == other.send_seq_num and
                self.data_generate_time == other.data_generate_time and
                self.data_packet_type == other.data_packet_type and
                self.data_packet_sender == other.data_packet_sender and
                self.data_packet_priority == other.data_packet_priority and
                self.body == other.body)

    # TODO: Expand validation criteria
    def validate_transmit_header(self):
        if self.send_time is None or self.send_seq_num is None:
            raise PacketFormatError("Packet not correctly defined")
        else:
            return True

    # TODO: Expand validation criteria
    def validate_data_header(self):
        if (self.data_generate_time is None or self.data_packet_type is None or self.data_packet_sender is None or
                self.data_packet_priority is None or self.body is None):
            raise PacketFormatError("Packet not correctly defined")
        else:
            return True

    def encode_packet(self):
        if self.is_radio:
            self.validate_transmit_header()

        self.validate_data_header()

        send_time_float = self.send_time.timestamp()
        send_seq_num_char = self.send_seq_num

        data_generate_time_float = self.data_generate_time.timestamp()
        data_packet_type_char = self.data_packet_type.value
        data_packet_sender_char = self.data_packet_sender.value
        data_packet_priority_char = self.data_packet_priority.value

        packet_bytes = struct.pack(definitions.struct_format_string, send_time_float, send_seq_num_char,
                                   data_generate_time_float, data_packet_type_char, data_packet_sender_char,
                                   data_packet_priority_char)
        packet_bytes += self.body
        return packet_bytes


def decode_packet(packet_bytes: bytes):
    header_bytes = packet_bytes[0:struct.calcsize(definitions.struct_format_string)]
    unpacked = struct.unpack(definitions.struct_format_string, header_bytes)

    send_timestamp = datetime.datetime.fromtimestamp(unpacked[0])
    send_seq_num = unpacked[1]
    data_generate_time = datetime.datetime.fromtimestamp(unpacked[2])
    data_packet_type = definitions.PacketType(unpacked[3])
    data_packet_device = definitions.Device(unpacked[4])
    data_packet_priority = definitions.Priority(unpacked[5])

    data_packet_body = packet_bytes[struct.calcsize(definitions.struct_format_string):]

    decoded_packet = Packet(send_timestamp, send_seq_num, data_generate_time, data_packet_type, data_packet_device,
                            data_packet_priority, data_packet_body)

    return decoded_packet
