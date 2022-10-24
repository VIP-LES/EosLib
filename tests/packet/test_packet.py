import pytest
import EosLib.packet.definitions as definitions

from datetime import datetime
from EosLib.packet.packet import TransmitHeader, DataHeader, Packet, PacketFormatError
from EosLib.packet.exceptions import DataHeaderFormatError, TransmitHeaderFormatError


def get_valid_packet():
    transmit_header = TransmitHeader(0, datetime.now())
    data_header = DataHeader(definitions.PacketType.TELEMETRY,
                             definitions.PacketDevice.GPS,
                             definitions.PacketPriority.TELEMETRY,
                             datetime.now())

    return Packet(bytes("Hello World", 'utf-8'), data_header, transmit_header)


def test_validate_good_transmit_header():
    test_packet = get_valid_packet()
    assert test_packet.transmit_header.validate_transmit_header()


def test_validate_bad_transmit_header_num():
    test_packet = get_valid_packet()
    test_packet.transmit_header.send_seq_num = None
    with pytest.raises(TransmitHeaderFormatError):
        test_packet.transmit_header.validate_transmit_header()


def test_validate_bad_transmit_header_time():
    test_packet = get_valid_packet()
    test_packet.transmit_header.send_time = None
    with pytest.raises(TransmitHeaderFormatError):
        test_packet.transmit_header.validate_transmit_header()


def test_validate_good_data_header():
    test_packet = get_valid_packet()
    assert test_packet.data_header.validate_data_header()


def test_validate_bad_data_header_type():
    test_packet = get_valid_packet()
    test_packet.data_header.data_packet_type = None
    with pytest.raises(DataHeaderFormatError):
        test_packet.data_header.validate_data_header()


def test_validate_bad_data_sender():
    test_packet = get_valid_packet()
    test_packet.data_header.data_packet_sender = 256
    with pytest.raises(DataHeaderFormatError):
        test_packet.data_header.validate_data_header()


def test_validate_bad_data_priority():
    test_packet = get_valid_packet()
    test_packet.data_header.data_packet_priority = 256
    with pytest.raises(DataHeaderFormatError):
        test_packet.data_header.validate_data_header()


def test_validate_bad_data_time():
    test_packet = get_valid_packet()
    test_packet.data_header.data_packet_generate_time = None
    with pytest.raises(DataHeaderFormatError):
        test_packet.data_header.validate_data_header()


def test_validate_body_only_packet():
    model_packet = get_valid_packet()

    model_packet.transmit_header = None
    model_packet.data_header = None

    with pytest.raises(PacketFormatError):
        model_packet.encode_packet()


def test_validate_empty_body_packet():
    model_packet = get_valid_packet()
    model_packet.body = None

    with pytest.raises(PacketFormatError):
        model_packet.encode_packet()


def test_encode_decode_packet():
    model_packet = get_valid_packet()
    test_packet = get_valid_packet()

    encoded_packet = test_packet.encode_packet()
    decoded_packet = Packet.decode_packet(encoded_packet)

    assert model_packet == decoded_packet


def test_encode_decode_data_only_packet():
    model_packet = get_valid_packet()
    test_packet = get_valid_packet()

    model_packet.transmit_header = None
    test_packet.transmit_header = None

    encoded_packet = test_packet.encode_packet()
    decoded_packet = Packet.decode_packet(encoded_packet)

    assert model_packet == decoded_packet


def test_body_too_large():
    test_packet = get_valid_packet()
    test_packet.body = bytearray(250)
    with pytest.raises(PacketFormatError):
        test_packet.encode_packet()


def test_allow_large_body_no_transmit():
    test_packet = get_valid_packet()
    test_packet.body = bytearray(250)
    test_packet.data_header.data_packet_priority = definitions.PacketPriority.NO_TRANSMIT

    assert test_packet.encode_packet()


def test_standalone_data_header_validate():
    test_header = bytearray(10)

    with pytest.raises(PacketFormatError):
        DataHeader.decode(test_header)


def test_standalone_transmit_header_validate():
    test_header = bytearray(10)

    with pytest.raises(PacketFormatError):
        TransmitHeader.decode(test_header)
