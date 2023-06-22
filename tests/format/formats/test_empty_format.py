import pytest

from EosLib.format.formats.empty_format import EmptyFormat

from tests.format.formats.format_test import CheckFormat


@pytest.mark.parametrize("test_size", [0, 5, 100])
def test_empty_format_length(test_size):
    test_format = EmptyFormat(test_size)
    assert len(test_format.encode()) == test_size


class TestEmptyFormat(CheckFormat):
    def get_format_from_list(self, format_list: []):
        return EmptyFormat(format_list[0])

    def get_good_format_list(self):
        return [5]
