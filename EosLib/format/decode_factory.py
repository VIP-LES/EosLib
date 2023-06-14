from EosLib.format import csv_format


class DecodeFactory:
    def __init__(self):
        self._decoders = {}
        self._csv_decoders = {}

    def register_decoder(self, format_class):
        self._decoders[format_class.get_format_type()] = format_class.decode
        if issubclass(format_class, csv_format.CsvFormat):
            self._csv_decoders[format_class.get_format_type()] = format_class.decode_from_csv

    def decode(self, data_format, data: bytes):
        decoder = self._decoders.get(data_format)
        if decoder is None:
            raise TypeError("No decoder found for this type")
        return decoder(data)

    def decode_from_csv(self, data_format, data: str):
        decoder = self._csv_decoders.get(data_format)
        if decoder is None:
            raise TypeError("No decoder found for this type")
        return decoder(data)


decode_factory = DecodeFactory()
