import math
import struct

from datetime import datetime
from EosLib.packet import definitions
from EosLib.packet.definitions import HeaderPreamble
from EosLib.packet.exceptions import PacketFormatError, DataHeaderFormatError


class DataHeader:

    data_header_struct_format_string = "!" \
                                       "B" \
                                       "B" \
                                       "B" \
                                       "B" \
                                       "d"

    def __init__(self,
                 data_packet_type: definitions.PacketType = None,
                 data_packet_sender: definitions.Device = None,
                 data_packet_priority: definitions.PacketPriority = None,
                 data_packet_generate_time: datetime = datetime.now()
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
        if not isinstance(self.data_packet_sender, int) or not 0 <= self.data_packet_sender <= 255:
            raise DataHeaderFormatError("Invalid Sender")

        if not isinstance(self.data_packet_type, int) or not 0 <= self.data_packet_type <= 255:
            raise DataHeaderFormatError("Invalid Type")

        if not isinstance(self.data_packet_priority, int) or not 0 <= self.data_packet_priority <= 255:
            raise DataHeaderFormatError("Invalid Priority")

        if not isinstance(self.data_packet_generate_time, datetime):
            raise DataHeaderFormatError("Invalid Generate Time")

        return True

    def encode(self):
        """ Checks that the header is valid and returns a bytes object if it is.

        :return: A bytes object containing the encoded header
        """
        self.validate_data_header()
        return struct.pack(DataHeader.data_header_struct_format_string,
                           HeaderPreamble.DATA,
                           self.data_packet_type,
                           self.data_packet_sender,
                           self.data_packet_priority,
                           self.data_packet_generate_time.timestamp())

    @staticmethod
    def decode(header_bytes: bytes):
        """Checks if the given bytes start with a DataHeader and, if so, decodes it.

        :param header_bytes: The bytes containing a data header at the front
        :return:
        """
        if header_bytes[0] != HeaderPreamble.DATA:
            raise PacketFormatError("Not a valid data header")

        unpacked = struct.unpack(DataHeader.data_header_struct_format_string, header_bytes)
        decoded_header = DataHeader(unpacked[1], unpacked[2], unpacked[3], datetime.fromtimestamp(unpacked[4]))
        return decoded_header
