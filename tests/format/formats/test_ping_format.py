from EosLib.format.formats.ping_format import Ping
from tests.format.formats.format_test import CheckFormat


good_data_list = [True, 223]


def get_ping_data_from_list(data_list: [int]):
    return Ping(good_data_list[0], good_data_list[1])


def get_good_ping_data():
    return get_ping_data_from_list(good_data_list)


def test_get_validity_valid():
    good_data = get_good_ping_data()
    assert good_data.get_validity()


def test_get_validity_bad_ack_lower():
    bad_sender_data = get_good_ping_data()
    bad_sender_data.num = -1
    assert not bad_sender_data.get_validity()


def test_get_validity_bad_ack_upper():
    bad_sender_data = get_good_ping_data()
    bad_sender_data.num = 256
    assert not bad_sender_data.get_validity()


def test_terminal_output_string():
    good_sender_data = get_good_ping_data()
    good_sender_data.ping_ack = True
    good_sender_data.num = 1
    assert good_sender_data.to_terminal_output_string() == "Received Ping: 1"


class TestPing(CheckFormat):

    def get_format(self):
        return Ping

    def get_good_format_params(self):
        return good_data_list
