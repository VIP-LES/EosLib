import datetime

from EosLib.format.formats.cutdown import CutDown

from tests.format.formats.csv_format_test import CheckCsvFormat

good_data_list = [datetime.datetime.now(), 1, 2, 3, 4, 5]


def get_cut_down_data_from_list(data_list: [float]):
    return CutDown(data_list[0],
                   data_list[1],
                   data_list[2],
                   data_list[3],
                   data_list[4],
                   data_list[5])


def get_good_cut_down_data():
    return get_cut_down_data_from_list(good_data_list)


def test_get_validity_valid():
    good_data = get_good_cut_down_data()
    assert good_data.get_validity()


def test_get_validity_bad_sender():
    bad_sender_data = get_good_cut_down_data()
    bad_sender_data.sender = None
    assert not bad_sender_data.get_validity()


def test_get_validity_bad_destination():
    bad_destination_data = get_good_cut_down_data()
    bad_destination_data.destination = None
    assert not bad_destination_data.get_validity()


class TestCutDownData(CheckCsvFormat):

    def get_format(self):
        return CutDown

    def get_good_format_params(self):
        return good_data_list
