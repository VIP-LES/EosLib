import abc
import copy
import datetime

import EosLib.format.csv_format
from EosLib.format.decode_factory import decode_factory


# Name can't contain the word Test, hence Check
class CheckFormat(abc.ABC):
    @abc.abstractmethod
    def get_format_from_list(self, format_list: []):
        raise NotImplementedError

    @abc.abstractmethod
    def get_good_format_list(self):
        raise NotImplementedError

    def get_good_format(self):
        return self.get_format_from_list(self.get_good_format_list())

    def test_is_eq(self):
        data_1 = self.get_good_format()
        data_2 = self.get_good_format()

        assert data_1 == data_2

    def test_not_eq(self):
        test_passed = True

        data_1 = self.get_good_format()

        for i in range(len(self.get_good_format_list())):
            new_data_list = copy.deepcopy(self.get_good_format_list())
            if isinstance(new_data_list[i], (int, float)):
                new_data_list[i] += 1
            elif isinstance(new_data_list[i], datetime.datetime):
                new_data_list[i] += datetime.timedelta(1)
            data_2 = self.get_format_from_list(new_data_list)

            if data_1 == data_2:
                test_passed = False

        assert test_passed

    def test_encode_decode_bytes(self):
        base_format = self.get_good_format()
        base_position_bytes = base_format.encode()
        new_format = decode_factory.decode(self.get_good_format().get_format_type(), base_position_bytes)
        assert base_format == new_format

