import datetime


def test_validate_transmit_header():
    from EosLib.packet.packet import Packet
    test_packet = Packet(send_time=datetime.datetime.now(), send_seq_num=0, is_radio=True)
    assert test_packet.validate_transmit_header()


def test_validate_data_header():
    assert False


def test_encode_packet():
    assert False
