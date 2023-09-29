import datetime

from EosLib.format.formats.position import Position
from EosLib.format.formats.position import FlightState

from tests.format.formats.csv_format_test import CheckCsvFormat

good_data_list = [datetime.datetime.now(),
                  33.7756,
                  84.3963,
                  974.5,
                  70.2,
                  5,
                  FlightState.DESCENT]


def get_position_from_list(position_list: [float]):
    return Position(position_list[0],
                    position_list[1],
                    position_list[2],
                    position_list[3],
                    position_list[4],
                    position_list[5],
                    position_list[6])


def get_good_position():
    return get_position_from_list(good_data_list)


def test_get_validity_valid():
    good_position = get_good_position()
    assert good_position.get_validity()


def test_get_validity_bad_satellites():
    bad_satellites_position = get_good_position()
    bad_satellites_position.number_of_satellites = 3
    assert not bad_satellites_position.get_validity()


class TestPosition(CheckCsvFormat):

    def get_format_class(self):
        return Position

    def get_good_format_params(self):
        return good_data_list
