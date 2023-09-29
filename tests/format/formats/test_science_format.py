from datetime import datetime, timedelta
from typing import Type
import copy

from EosLib.format.base_format import BaseFormat
from EosLib.format.formats.science_data import ScienceData
from tests.format.formats.csv_format_test import CheckCsvFormat


good_format_params = [
    26.38,              # temperature
    39.72,              # relative_humidity
    26.99,              # temperature_2
    981.3804861416284,  # pressure
    268.7146768726267,  # altitude
    579,                # light
    463.2,              # uv lux
    0,                  # uvs
    0.0,                # uvi
    376,                # infrared
    24643214,           # visible
    24643590,           # full_spectrum
    463.9,              # ir lux
    11,                 # pm10_standard
    24,                 # pm25_standard
    26,                 # pm100_standard
    11,                 # pm10_env
    24,                 # pm25_env
    26,                 # pm100_env
    1815,               # part_03
    567,                # part_05
    191,                # part_10
    13,                 # part_25
    3,                  # part_50
    3,                  # part_100
    datetime.fromisoformat("2023-06-29T04:02:34.294887"),  # timestamp, clearly
]


class TestScienceFormat(CheckCsvFormat):

    def get_format_class(self) -> Type[BaseFormat]:
        return ScienceData

    def get_good_format_params(self) -> list:
        return good_format_params

    # overriding to exclude timestamp from comparison, it is not used in the binary encoding
    def test_not_eq(self):
        data_1 = self.get_good_format()

        # Iterates over each parameter given in get_good_format_list, creating a new instance of the format with that
        # parameter modified. It then verifies that this modification causes the instances to evaluate as not equal.
        for i in range(len(self.get_good_format_params()) - 1):  # exclude timestamp
            new_data_list = copy.deepcopy(self.get_good_format_params())

            # Modifies current parameter
            if isinstance(new_data_list[i], (int, float)):
                new_data_list[i] += 1
            elif isinstance(new_data_list[i], datetime):
                new_data_list[i] += timedelta(1)

            data_2 = self.get_format_class()(*new_data_list)

            assert data_1 != data_2
