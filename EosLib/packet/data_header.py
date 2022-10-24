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
                 data_type: definitions.PacketType = None,
                 sender: definitions.PacketDevice = None,
                 priority: definitions.PacketPriority = None,
                 generate_time: datetime = datetime.now()
                 ):
        self.sender = sender
        self.data_type = data_type
        self.priority = priority
        self.generate_time = generate_time

    def __eq__(self, other):
        return (self.priority == other.priority and
                self.data_type == other.data_type and
                self.sender == other.sender and
                math.isclose(self.generate_time.timestamp(), other.generate_time.timestamp()))

    # TODO: Expand validation criteria
    def validate_data_header(self):
        """Checks that all fields in the TransmitHeader object are valid and throws an exception if they aren't.

        :return: True if valid
        """
        if not isinstance(self.sender, int) or not 0 <= self.sender <= 255:
            raise DataHeaderFormatError("Invalid Sender")

        if not isinstance(self.data_type, int) or not 0 <= self.data_type <= 255:
            raise DataHeaderFormatError("Invalid Type")

        if not isinstance(self.priority, int) or not 0 <= self.priority <= 255:
            raise DataHeaderFormatError("Invalid Priority")

        if not isinstance(self.generate_time, datetime):
            raise DataHeaderFormatError("Invalid Generate Time")

        return True

    def encode(self):
        """ Checks that the header is valid and returns a bytes object if it is.

        :return: A bytes object containing the encoded header
        """
        self.validate_data_header()
        return struct.pack(DataHeader.data_header_struct_format_string,
                           HeaderPreamble.DATA,
                           self.data_type,
                           self.sender,
                           self.priority,
                           self.generate_time.timestamp())

    def encode_to_string(self):
        self.validate_data_header()
        return "{data_type}, {sender}, {priority}, {generate_time}".format(data_type=self.data_type,
                                                                           sender=self.sender,
                                                                           priority=self.priority,
                                                                           generate_time=self.generate_time.isoformat())

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
