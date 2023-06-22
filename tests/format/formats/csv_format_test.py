from abc import ABC

from tests.format.formats.format_test import CheckFormat

from EosLib.format.decode_factory import decode_factory


class CheckCsvFormat(CheckFormat, ABC):
    def test_encode_decode_csv(self):
        base_format = self.get_good_format()
        base_format_csv = base_format.encode_to_csv()
        new_position = decode_factory.decode(self.get_good_format().get_format_type(), base_format_csv)

        assert base_format == new_position
