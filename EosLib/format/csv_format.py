from abc import ABC
from abc import abstractmethod
from typing_extensions import Self

from EosLib.format.base_format import BaseFormat


class CsvFormat(BaseFormat, ABC):
    @classmethod
    def get_decoders(cls) -> {}:
        return {bytes: cls.decode,
                str: cls.decode_from_csv}

    @abstractmethod
    def get_csv_headers(self):
        raise NotImplementedError

    @abstractmethod
    def encode_to_csv(self) -> str:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def decode_from_csv(cls, csv_string: str) -> Self:
        raise NotImplementedError
