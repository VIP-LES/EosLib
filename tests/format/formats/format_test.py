from typing import Type
import abc
import copy
import datetime

from EosLib.format.base_format import BaseFormat
from EosLib.format.decode_factory import decode_factory


# Name can't contain the word Test, hence Check
class CheckFormat(abc.ABC):

    @abc.abstractmethod
    def get_format_class(self) -> Type[BaseFormat]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_good_format_params(self) -> list:
        """Provides a list of parameters that can be used by get_format_from_list to generate a valid instance of
        the format. Used to automate validating __eq__()"""
        raise NotImplementedError

    def get_good_format(self) -> BaseFormat:
        """Returns a valid instance of the format being tested. This is a helper function combining get_good_format_list
        and get_format_from_list."""
        return self.get_format_class()(*self.get_good_format_params())

    def test_is_eq(self):
        data_1 = self.get_good_format()
        data_2 = self.get_good_format()

        assert data_1 == data_2

    def test_not_eq(self):
        data_1 = self.get_good_format()

        # Iterates over each parameter given in get_good_format_list, creating a new instance of the format with that
        # parameter modified. It then verifies that this modification causes the instances to evaluate as not equal.
        for i in range(len(self.get_good_format_params())):
            new_data_list = copy.deepcopy(self.get_good_format_params())

            # Modifies current parameter
            if isinstance(new_data_list[i], (int, float)):
                new_data_list[i] += 1
            elif isinstance(new_data_list[i], datetime.datetime):
                new_data_list[i] += datetime.timedelta(1)
            elif isinstance(new_data_list[i], list):
                continue

            data_2 = self.get_format_class()(*new_data_list)

            assert data_1 != data_2

    def test_encode_decode_bytes(self):
        base_format = self.get_good_format()
        base_position_bytes = base_format.encode()
        new_format = decode_factory.decode(self.get_good_format().get_format_type(), base_position_bytes)
        assert base_format == new_format

    def test_get_validity_happy_path(self):
        assert self.get_good_format().get_validity()
