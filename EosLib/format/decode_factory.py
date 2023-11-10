from typing import Any
from EosLib.format.definitions import Type


class DecodeFactory:
    def __init__(self):
        self._decoders: dict[Type, dict] = {}

    def register_decoder(self, format_class):
        self._decoders[format_class.get_format_type()] = format_class.get_decoders()

    def decode(self, data_format: Type, data: Any):
        decoders_for_format = self._decoders.get(data_format)
        if decoders_for_format is None:
            raise TypeError(f"No decoders found for format type {Type(data_format).name}")
        if isinstance(data, bytearray):
            data = bytes(data)
        decoder = decoders_for_format.get(type(data))
        if decoder is None:
            raise TypeError(f"No decoder found for format type {Type(data_format).name} for data type {type(data)}."
                            + "  Decoders are defined for: " + ', '.join([str(key) for key in self._decoders.get(data_format).keys()]))
        return decoder(data)


decode_factory = DecodeFactory()
