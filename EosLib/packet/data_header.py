import math
import struct
from datetime import datetime

from EosLib.packet import definitions
from EosLib.packet.definitions import PacketFormatError


class DataHeader:
    def __init__(self, data_packet_generate_time: datetime = datetime.now(),
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
        """Checks that all fields in the TransmitHeader object are valid and throws an exception if they aren't.

        :return: True if valid
        """
        if (self.data_packet_sender is None or self.data_packet_type is None or
                self.data_packet_priority is None or self.data_packet_generate_time is None):
            raise PacketFormatError("Data header has invalid value")
        return True

    def encode(self):
        """ Checks that the header is valid and returns a bytes object if it is.

        :return: A bytes object containing the encoded header
        """
        self.validate_data_header()
        return struct.pack(definitions.data_header_struct_format_string, definitions.data_header_preamble,
                           self.data_packet_generate_time.timestamp(), self.data_packet_type, self.data_packet_sender,
                           self.data_packet_priority)
