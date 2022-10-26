import datetime
import struct


from EosLib.packet.transmit_header import TransmitHeader
from EosLib.packet.data_header import DataHeader
from EosLib.packet.definitions import HeaderPreamble, PacketPriority, RADIO_MAX_BYTES
from EosLib.packet.exceptions import PacketFormatError


class Packet:
    def __init__(self, body: bytes = None, data_header: DataHeader = None, transmit_header: TransmitHeader = None):
        """Initializes a Packet object

        :param body: A bytes object containing the body of the packet
        :param data_header: A DataHeader object to be added to the packet
        :param transmit_header: A TransmitHeader object to be added to the packet
        """
        self.body = body  # type: bytes
        self.data_header = data_header  # type: DataHeader
        self.transmit_header = transmit_header  # type: TransmitHeader

    def __eq__(self, other):
        return (self.data_header == other.data_header and
                self.transmit_header == other.transmit_header and
                self.body == other.body)

    def validate_packet(self):
        if self.data_header is None:
            raise PacketFormatError("All packets must have a data header")
        else:
            self.data_header.validate_data_header()

        if self.transmit_header is not None:
            self.transmit_header.validate_transmit_header()

        if self.body is None or len(self.body) == 0:
            raise PacketFormatError("All packets must have a body")

        if not isinstance(self.body, bytes):
            raise PacketFormatError("Body should be of type bytes")

        if self.data_header.priority != PacketPriority.NO_TRANSMIT:
            total_length = struct.calcsize(TransmitHeader.transmit_header_struct_format_string) + \
                           struct.calcsize(DataHeader.data_header_struct_format_string) + \
                           len(self.body)

            if total_length > RADIO_MAX_BYTES:
                raise PacketFormatError("Packet is too large")

        return True

    def encode(self) -> bytes:
        """Validates and then returns the byte string version of the initialized packet.

        :return: Validated packet byte string
        """

        self.validate_packet()

        packet_bytes = b''

        if self.transmit_header is not None:
            packet_bytes += self.transmit_header.encode()

        packet_bytes += self.data_header.encode()

        packet_bytes += self.body

        return packet_bytes

    def encode_to_string(self):
        self.validate_packet()

        return "{transmit_header}, {data_header}, {body}".format(
            transmit_header=self.transmit_header.encode_to_string(),
            data_header=self.data_header.encode_to_string(),
            body=self.body.decode())

    @staticmethod
    def decode(packet_bytes: bytes):
        """Takes a bytes object and decodes it into a Packet object.

        :param packet_bytes: The bytes object to be decoded
        :return: The decoded Packet object
        """
        decoded_packet = Packet()
        if packet_bytes[0] == HeaderPreamble.TRANSMIT:
            decoded_transmit_header = TransmitHeader.decode(
                packet_bytes[0:struct.calcsize(TransmitHeader.transmit_header_struct_format_string)])
            decoded_packet.transmit_header = decoded_transmit_header
            packet_bytes = packet_bytes[struct.calcsize(TransmitHeader.transmit_header_struct_format_string):]

        if packet_bytes[0] == HeaderPreamble.DATA:
            decoded_data_header = DataHeader.decode(
                packet_bytes[0:struct.calcsize(DataHeader.data_header_struct_format_string)])
            decoded_packet.data_header = decoded_data_header
            packet_bytes = packet_bytes[struct.calcsize(DataHeader.data_header_struct_format_string):]

        decoded_packet.body = packet_bytes

        return decoded_packet

    @staticmethod
    def decode_from_string(packet_string: str):
        """Takes a string and decodes it into a Packet object.

        :param packet_string: The string to be decoded
        :return: The decoded Packet object
        """

        decoded_packet = Packet()
        decoded_transmit_header = TransmitHeader()
        decoded_data_header = DataHeader()

        packet_array = packet_string.split(', ')

        decoded_transmit_header.send_seq_num = int(packet_array[0])
        decoded_transmit_header.send_time = datetime.datetime.fromisoformat(packet_array[1])

        decoded_data_header.data_type = int(packet_array[2])
        decoded_data_header.sender = int(packet_array[3])
        decoded_data_header.priority = int(packet_array[4])
        decoded_data_header.generate_time = datetime.datetime.fromisoformat(packet_array[5])

        decoded_packet.transmit_header = decoded_transmit_header
        decoded_packet.data_header = decoded_data_header
        decoded_packet.body = bytes(packet_array[6], 'utf-8')

        return decoded_packet
