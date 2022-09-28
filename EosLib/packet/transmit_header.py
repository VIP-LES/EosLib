import math
import struct
from datetime import datetime

from EosLib.packet.definitions import PacketFormatError


class TransmitHeader:

    transmit_header_preamble = 1
    transmit_header_struct_format_string = "!" \
                                           "B" \
                                           "B" \
                                           "d"

    def __init__(self, send_seq_num: int, send_time: datetime = datetime.now()):
        """Initializes a TransmitHeader object

        :param send_seq_num: The sequence number assigned at the transmitter
        :param send_time: The time the packet is sent to the transmitter
        """
        self.send_seq_num = send_seq_num
        self.send_time = send_time

    def __eq__(self, other):
        return (self.send_seq_num == other.send_seq_num and
                math.isclose(self.send_time.timestamp(), other.send_time.timestamp()))

    # TODO: Expand validation criteria
    def validate_transmit_header(self):
        """Checks that all fields in the TransmitHeader object are valid and throws an exception if they aren't.

        :return: True if valid
        """
        if self.send_time is None or self.send_seq_num is None:
            raise PacketFormatError("Transmit header has invalid value")
        return True

    def encode(self):
        """ Checks that the header is valid and returns a bytes object if it is.

        :return: A bytes object containing the encoded header
        """
        self.validate_transmit_header()
        return struct.pack(TransmitHeader.transmit_header_struct_format_string, TransmitHeader.transmit_header_preamble,
                           self.send_seq_num, self.send_time.timestamp())

    @staticmethod
    def decode(header_bytes: bytes):
        """Checks if the given bytes start with a TransmitHeader and, if so, decodes it.

        :param header_bytes: The bytes containing a transmit header at the front
        :return: a decoded TransmitHeader
        """
        if header_bytes[0] != TransmitHeader.transmit_header_preamble:
            raise PacketFormatError("Not a valid transmit header")

        unpacked = struct.unpack(TransmitHeader.transmit_header_struct_format_string, header_bytes)
        decoded_header = TransmitHeader(unpacked[1], datetime.fromtimestamp(unpacked[2]))
        return decoded_header

