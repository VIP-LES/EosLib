from EosLib.format.formats.empty_format import EmptyFormat

from tests.format.formats.format_test import CheckFormat


class TestEmptyFormat(CheckFormat):
    def get_format_from_list(self, format_list: []):
        return EmptyFormat()

    def get_good_format_list(self):
        return []
