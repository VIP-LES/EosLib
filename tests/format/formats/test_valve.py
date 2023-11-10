from EosLib.format.formats.valve import Valve
from tests.format.formats.format_test import CheckFormat


good_data_list = [1]


def get_valve_data_from_list(data_list: [int]):
    return Valve(data_list[0])


def get_good_valve_data():
    return get_valve_data_from_list(good_data_list)


def test_get_validity_valid():
    good_data = get_good_valve_data()
    assert good_data.get_validity()


def test_get_validity_bad_ack_lower():
    bad_sender_data = get_good_valve_data()
    bad_sender_data.ack = -1
    assert not bad_sender_data.get_validity()


def test_get_validity_bad_ack_upper():
    bad_sender_data = get_good_valve_data()
    bad_sender_data.ack = 256
    assert not bad_sender_data.get_validity()


def test_terminal_output_string():
    good_sender_data = get_good_valve_data()
    good_sender_data.ack = 1
    assert good_sender_data.to_terminal_output_string() == "Received valve ACK: 1"


class TestValve(CheckFormat):

    def get_format_class(self):
        return Valve

    def get_good_format_params(self):
        return good_data_list
