import struct

from EosLib.device import Device
import EosLib.format.decode_factory
from EosLib.format.base_format import BaseFormat
from EosLib.format.definitions import Type

from EosLib.packet.transmit_header import TransmitHeader
from EosLib.packet.data_header import DataHeader
from EosLib.packet.definitions import HeaderPreamble, Priority
from EosLib.packet.exceptions import PacketFormatError


class Packet:
    radio_max_bytes = 255
    radio_body_max_bytes = radio_max_bytes - (struct.calcsize(TransmitHeader.transmit_header_struct_format_string)
                                              + struct.calcsize(DataHeader.data_header_struct_format_string))

    def __init__(self, body: BaseFormat, data_header: DataHeader, transmit_header: TransmitHeader = None):
        """Initializes a Packet object

        :param body: A bytes object containing the body of the packet
        :param data_header: A DataHeader object to be added to the packet
        :param transmit_header: A TransmitHeader object to be added to the packet
        """
        self.body = body
        self.data_header = data_header
        self.transmit_header = transmit_header

    def __eq__(self, other):
        """ Compares two packets for value equality

        :param other: the other packet to be compared
        :return: True if packets are equal, False otherwise
        """
        return (self.data_header == other.data_header and
                self.transmit_header == other.transmit_header and
                self.body == other.body)

    def __str__(self):
        """ Creates a readable representation of the current packet

        :return: A readable representation of the packet
        """
        output_string = ""
        if self.transmit_header is None:
            output_string += "No transmit header\n"
        else:
            output_string += f"Transmit Header:\n" \
                             f"\tSend time:{self.transmit_header.send_time}\n" \
                             f"\tSequence number: {self.transmit_header.send_seq_num}\n" \
                             f"\tRSSI: {self.transmit_header.send_rssi}\n"

        if self.data_header is None:
            output_string += "No data header\n"
        else:
            output_string += f"Data Header:\n" \
                             f"\tSender: {Device(self.data_header.sender).name}\n" \
                             f"\tData type: {Type(self.data_header.data_type).name}\n" \
                             f"\tPriority: {Priority(self.data_header.priority).name}\n" \
                             f"\tDestination: {Device(self.data_header.destination).name}\n" \
                             f"\tGenerate Time: {self.data_header.generate_time}\n"

        if self.body is None:
            output_string += "No body"
        else:
            output_string += f"Body: {self.body}"

        return output_string

    def validate_packet(self):
        """ Validates that all fields in the packet are valid and throws an exception if they aren't

        :return: True if packet is valid

        :raises: PacketFormatError if packet is not valid
        """
        if self.data_header is None:
            raise PacketFormatError("All packets must have a data header")
        else:
            self.data_header.validate_data_header()

        if self.transmit_header is not None:
            self.transmit_header.validate_transmit_header()

        if not issubclass(self.body.__class__, BaseFormat):
            raise PacketFormatError("All packets must have a body that extends BaseFormat")

        # TODO make it so packet headers must be valid
        # if self.body.get_validity() is False:
            # raise PacketFormatError("All packets must contain a valid format")

        if self.data_header.priority != Priority.NO_TRANSMIT:
            total_length = struct.calcsize(TransmitHeader.transmit_header_struct_format_string) + \
                           struct.calcsize(DataHeader.data_header_struct_format_string) + \
                           len(self.body.encode())

            if total_length > Packet.radio_max_bytes:
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

        packet_bytes += self.body.encode()

        return packet_bytes

    @staticmethod
    def decode(packet_bytes: bytes):
        """Takes a bytes object and decodes it into a Packet object.

        :param packet_bytes: The bytes object to be decoded
        :return: The decoded Packet object
        """

        if packet_bytes[0] == HeaderPreamble.TRANSMIT:
            decoded_transmit_header = TransmitHeader.decode(
                packet_bytes[0:struct.calcsize(TransmitHeader.transmit_header_struct_format_string)])

            decoded_transmit_header = decoded_transmit_header
            packet_bytes = packet_bytes[struct.calcsize(TransmitHeader.transmit_header_struct_format_string):]
        else:
            decoded_transmit_header = None

        if packet_bytes[0] == HeaderPreamble.DATA:
            decoded_data_header = DataHeader.decode(
                packet_bytes[0:struct.calcsize(DataHeader.data_header_struct_format_string)])
            decoded_data_header = decoded_data_header
            packet_bytes = packet_bytes[struct.calcsize(DataHeader.data_header_struct_format_string):]
        else:
            decoded_data_header = None
            #raise PacketFormatError(f"Packet does not contain a header. Unexpected packet header: {packet_bytes[0]}, should be: {HeaderPreamble.DATA}")

        decoded_packet = Packet(EosLib.format.decode_factory.decode_factory.decode(decoded_data_header.data_type,
                                                                                   packet_bytes),
                                decoded_data_header,
                                decoded_transmit_header)

        return decoded_packet
