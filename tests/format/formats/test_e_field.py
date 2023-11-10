import pytest

from EosLib.format.formats.e_field import EField

from tests.format.formats.csv_format_test import CheckCsvFormat

good_data_list = [0, 1.4999, 0.5]


def get_e_field_data_from_list(data_list: [float]):
    return EField(data_list[0],
                  data_list[1],
                  data_list[2])


def get_good_e_field_data():
    return get_e_field_data_from_list(good_data_list)


def test_get_validity_valid():
    good_data = get_good_e_field_data()
    assert good_data.get_validity()


@pytest.mark.parametrize("bad_voltage", [-10, -0.000001, 1.5000001, 10])
def test_get_validity_bad_voltages(bad_voltage):
    bad_voltages = get_good_e_field_data()
    bad_voltages.voltage_b = bad_voltage
    assert not bad_voltages.get_validity()


class TestEField(CheckCsvFormat):

    def get_format_class(self):
        return EField

    def get_good_format_params(self):
        return good_data_list
