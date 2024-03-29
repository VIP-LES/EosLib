import pytest

import EosLib.format.base_format
import EosLib.format.definitions
import EosLib.packet.definitions as definitions

from EosLib.format.formats.empty_format import EmptyFormat
from EosLib.format.formats.e_field import EField

from datetime import datetime

from EosLib.packet.packet import TransmitHeader, DataHeader, Packet, PacketFormatError
from EosLib.packet.exceptions import DataHeaderFormatError, TransmitHeaderFormatError
from EosLib.device import Device


def get_valid_packet():
    transmit_header = TransmitHeader(0, datetime.now(), 0)
    data_header = DataHeader(Device.GPS,
                             EosLib.format.definitions.Type.EMPTY,
                             definitions.Priority.TELEMETRY,
                             Device.GPS,
                             datetime.now())

    return Packet(EmptyFormat(0), data_header, transmit_header)


def test_minimal_constructor():
    data_header = DataHeader(Device.GPS)
    packet = Packet(EmptyFormat(0), data_header)
    packet.encode()


@pytest.fixture
def packet():
    return get_valid_packet()


def test_validate_good_transmit_header(packet):
    assert packet.transmit_header.validate_transmit_header()


@pytest.mark.parametrize("rssi", [0, -120])
def test_rssi_min_max_transmit_header(packet, rssi):
    packet.transmit_header.send_rssi = rssi
    assert packet.transmit_header.validate_transmit_header()


@pytest.mark.parametrize("send_seq_num", [0, 255, 3])
def test_validate_good_transmit_header_send_seq_num(packet, send_seq_num):
    packet.transmit_header.send_seq_num = send_seq_num
    assert packet.transmit_header.validate_transmit_header()


def test_validate_good_data_header(packet):
    assert packet.data_header.validate_data_header()


@pytest.mark.parametrize("sender", [Device.PRESSURE, max(Device), Device.GPS])
def test_validate_good_data_header_sender(packet, sender):
    packet.data_header.sender = sender
    assert packet.data_header.validate_data_header()


@pytest.mark.parametrize("data_type", [min(EosLib.format.definitions.Type), max(EosLib.format.definitions.Type),
                                       EosLib.format.definitions.Type.WARNING])
def test_validate_good_data_header_data_type(packet, data_type):
    packet.data_header.data_type = data_type
    assert packet.data_header.validate_data_header()


@pytest.mark.parametrize("priority", [min(definitions.Priority), max(definitions.Priority), definitions.Priority.DATA])
def test_validate_good_data_header_priority(packet, priority):
    packet.data_header.priority = priority
    assert packet.data_header.validate_data_header()


@pytest.mark.parametrize("destination", [min(Device), max(Device), Device.O3])
def test_validate_good_data_header_destination(packet, destination):
    packet.data_header.data_type = destination
    assert packet.data_header.validate_data_header()


@pytest.mark.parametrize("bad_data_value", [None, -200, 256, "String"])
class TestBadHeaders:
    """Tests for the packet's transmit header and data header, sharing bad data values."""

    def test_validate_bad_transmit_header_num(self, packet, bad_data_value):
        packet.transmit_header.send_seq_num = bad_data_value
        with pytest.raises(TransmitHeaderFormatError):
            packet.transmit_header.validate_transmit_header()

    def test_validate_bad_transmit_header_time(self, packet, bad_data_value):
        packet.transmit_header.send_time = bad_data_value
        with pytest.raises(TransmitHeaderFormatError):
            packet.transmit_header.validate_transmit_header()

    def test_validate_bad_transmit_header_rssi(self, packet, bad_data_value):
        packet.transmit_header.send_rssi = bad_data_value
        with pytest.raises(TransmitHeaderFormatError):
            packet.transmit_header.validate_transmit_header()

    def test_validate_bad_data_header_type(self, packet, bad_data_value):
        packet.data_header.data_type = bad_data_value
        with pytest.raises(DataHeaderFormatError):
            packet.data_header.validate_data_header()

    def test_validate_bad_data_sender(self, packet, bad_data_value):
        packet.data_header.sender = bad_data_value
        with pytest.raises(DataHeaderFormatError):
            packet.data_header.validate_data_header()

    def test_validate_bad_data_priority(self, packet, bad_data_value):
        packet.data_header.priority = bad_data_value
        with pytest.raises(DataHeaderFormatError):
            packet.data_header.validate_data_header()

    def test_validate_bad_destination(self, packet, bad_data_value):
        packet.data_header.destination = bad_data_value
        with pytest.raises(DataHeaderFormatError):
            packet.data_header.validate_data_header()

    def test_validate_bad_data_time(self, packet, bad_data_value):
        packet.data_header.generate_time = bad_data_value
        with pytest.raises(DataHeaderFormatError):
            packet.data_header.validate_data_header()


def test_validate_body_only_packet(packet):
    packet.transmit_header = None
    packet.data_header = None

    with pytest.raises(PacketFormatError):
        packet.encode()


def test_validate_empty_body_packet(packet):
    packet.body = None

    with pytest.raises(PacketFormatError):
        packet.encode()


def test_body_too_large(packet):
    packet.body = EmptyFormat(Packet.radio_body_max_bytes + 1)
    with pytest.raises(PacketFormatError):
        packet.encode()


@pytest.mark.parametrize("illegal_body", [None, "String"])
def test_illegal_body_type(packet, illegal_body):
    packet.body = illegal_body

    with pytest.raises(PacketFormatError):
        packet.encode()


def test_valid_body_format(packet):
    packet.body = EField(0, 1.5, 1)
    assert packet.body.get_validity()


def test_invalid_body_format(packet):
    packet.body = EField(-1, 1.5, 1)
    assert not packet.body.get_validity()


def test_allow_large_body_no_transmit(packet):
    packet.body = EmptyFormat(Packet.radio_body_max_bytes + 1)
    packet.data_header.priority = definitions.Priority.NO_TRANSMIT

    assert packet.encode()


def test_max_body_size(packet):
    packet.body = EmptyFormat(Packet.radio_body_max_bytes)
    assert packet.encode()


def test_standalone_data_header_validate():
    test_header = bytearray(10)

    with pytest.raises(PacketFormatError):
        DataHeader.decode(test_header)


def test_standalone_transmit_header_validate():
    test_header = bytearray(20)

    with pytest.raises(PacketFormatError):
        TransmitHeader.decode(test_header)


def test_encode_decode_packet(packet):
    model_packet = get_valid_packet()

    encoded_packet = packet.encode()
    decoded_packet = Packet.decode(encoded_packet)

    assert model_packet == decoded_packet


def test_encode_decode_data_only_packet(packet):
    model_packet = get_valid_packet()

    model_packet.transmit_header = None
    packet.transmit_header = None

    encoded_packet = packet.encode()
    decoded_packet = Packet.decode(encoded_packet)

    assert model_packet == decoded_packet


def test_old_data_header_version(packet):
    packet.transmit_header = None

    encoded_bytes = packet.encode()
    old_encoded_bytes = b'\x02' + encoded_bytes[1:]

    with pytest.raises(PacketFormatError):
        Packet.decode(old_encoded_bytes)


def test_packet_print_two_headers(packet):
    # Set the times to non-now times to be sure they aren't being overridden by datetime.now()
    packet.data_header.generate_time = datetime.fromisoformat("2001-01-07 01:23:45.000")
    packet.transmit_header.send_time = datetime.fromisoformat("2002-01-07 01:23:45.000")

    expected_string = "Transmit Header:\n" \
                      "\tSend time:2002-01-07 01:23:45\n" \
                      "\tSequence number: 0\n" \
                      "\tRSSI: 0\n" \
                      "Data Header:\n" \
                      "\tSender: GPS\n" \
                      "\tData type: EMPTY\n" \
                      "\tPriority: TELEMETRY\n" \
                      "\tDestination: GPS\n" \
                      "\tGenerate Time: 2001-01-07 01:23:45\n" \
                      "Body:"

    assert packet.__str__().startswith(expected_string)


def test_packet_data_header_only(packet):
    # Set the times to non-now times to be sure they aren't being overridden by datetime.now()
    packet.data_header.generate_time = datetime.fromisoformat("2001-01-07 01:23:45.000")

    packet.transmit_header = None

    expected_string = "No transmit header\n" \
                      "Data Header:\n" \
                      "\tSender: GPS\n" \
                      "\tData type: EMPTY\n" \
                      "\tPriority: TELEMETRY\n" \
                      "\tDestination: GPS\n" \
                      "\tGenerate Time: 2001-01-07 01:23:45\n" \
                      "Body:"

    assert packet.__str__().startswith(expected_string)


def test_packet_no_headers(packet):
    # This shouldn't ever happen, but is a possible state, so we should test for it.

    packet.data_header = None
    packet.transmit_header = None

    expected_string = "No transmit header\n" \
                      "No data header\n" \
                      "Body:"

    assert packet.__str__().startswith(expected_string)


def test_packet_print_no_body(packet):
    # Set the times to non-now times to be sure they aren't being overridden by datetime.now()
    packet.data_header.generate_time = datetime.fromisoformat("2001-01-07 01:23:45.000")
    packet.transmit_header.send_time = datetime.fromisoformat("2002-01-07 01:23:45.000")

    packet.body = None

    expected_string = "Transmit Header:\n" \
                      "\tSend time:2002-01-07 01:23:45\n" \
                      "\tSequence number: 0\n" \
                      "\tRSSI: 0\n" \
                      "Data Header:\n" \
                      "\tSender: GPS\n" \
                      "\tData type: EMPTY\n" \
                      "\tPriority: TELEMETRY\n" \
                      "\tDestination: GPS\n" \
                      "\tGenerate Time: 2001-01-07 01:23:45\n" \
                      "No body"

    assert expected_string == packet.__str__()
