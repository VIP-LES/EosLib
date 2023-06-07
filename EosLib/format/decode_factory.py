class DecodeFactory:
    def __init__(self):
        self._decoders = {}

    def register_decoder(self, format_class):
        self._decoders[format_class.get_format_type()] = format_class.decode

    def decode(self, data_format, data: bytes):
        return self._decoders[data_format](data)


decode_factory = DecodeFactory()
