import pytest

from EosLib.packet.packet import *


def get_valid_packet():
    return Packet(datetime.datetime.now(), 0, datetime.datetime.now(), definitions.PacketType.TELEMETRY,
                  definitions.Device.GPS, definitions.Priority.TELEMETRY, bytes("Hello World", 'utf-8'), True)


def test_validate_good_transmit_header():
    test_packet = get_valid_packet()
    assert test_packet.validate_transmit_header()


def test_validate_bad_transmit_header_num():
    test_packet = get_valid_packet()
    test_packet.send_seq_num = None
    with pytest.raises(PacketFormatError):
        test_packet.validate_transmit_header()


def test_validate_bad_transmit_header_time():
    test_packet = get_valid_packet()
    test_packet.send_time = None
    with pytest.raises(PacketFormatError):
        test_packet.validate_transmit_header()


def test_validate_data_header():
    test_packet = get_valid_packet()
    assert test_packet.validate_data_header()


def test_encode_decode_packet():
    model_packet = get_valid_packet()
    test_packet = get_valid_packet()

    encoded_packet = test_packet.encode_packet()
    decoded_packet = decode_packet(encoded_packet)

    assert model_packet == decoded_packet
