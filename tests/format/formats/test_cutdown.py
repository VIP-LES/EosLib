from EosLib.format.formats.cutdown import CutDown
from tests.format.formats.format_test import CheckFormat


good_data_list = [1]


def get_cut_down_data_from_list(data_list: [int]):
    return CutDown(data_list[0])


def get_good_cut_down_data():
    return get_cut_down_data_from_list(good_data_list)


def test_get_validity_valid():
    good_data = get_good_cut_down_data()
    assert good_data.get_validity()


def test_get_validity_bad_ack_lower():
    bad_sender_data = get_good_cut_down_data()
    bad_sender_data.ack = -1
    assert not bad_sender_data.get_validity()


def test_get_validity_bad_ack_upper():
    bad_sender_data = get_good_cut_down_data()
    bad_sender_data.ack = 256
    assert not bad_sender_data.get_validity()


class TestCutDown(CheckFormat):

    def get_format(self):
        return CutDown

    def get_good_format_params(self):
        return good_data_list
