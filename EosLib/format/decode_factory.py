from EosLib.format import csv_format


class DecodeFactory:
    def __init__(self):
        self._decoders = {}

    def register_decoder(self, format_class):
        self._decoders[format_class.get_format_type()] = format_class.get_decoders()

    def decode(self, data_format, data):
        decoder = self._decoders.get(data_format).get(type(data))
        if decoder is None:
            raise TypeError("No decoder found for this type")
        return decoder(data)


decode_factory = DecodeFactory()
