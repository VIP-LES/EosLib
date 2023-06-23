from EosLib.format.formats.telemetry_data import TelemetryData

from tests.format.formats.csv_format_test import CheckCsvFormat

good_data_list = [32.0, 1013.25, 50.5, 30.0, 45.0, 60.0]


def get_telemetry_data_from_list(data_list: [float]):
    return TelemetryData(data_list[0],
                         data_list[1],
                         data_list[2],
                         data_list[3],
                         data_list[4],
                         data_list[5])


def get_good_telemetry_data():
    return get_telemetry_data_from_list(good_data_list)


def test_get_validity_valid():
    good_data = get_good_telemetry_data()
    assert good_data.get_validity()


def test_get_validity_bad_humidity():
    bad_humidity_data = get_good_telemetry_data()
    bad_humidity_data.humidity = -1
    assert not bad_humidity_data.get_validity()


def test_get_validity_bad_pressure():
    bad_humidity_data = get_good_telemetry_data()
    bad_humidity_data.pressure = -1
    assert not bad_humidity_data.get_validity()


class TestTelemetryData(CheckCsvFormat):

    def get_format(self):
        return TelemetryData

    def get_good_format_params(self):
        return good_data_list
