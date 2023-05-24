from abc import ABC
from abc import abstractmethod
from typing_extensions import Self

from EosLib.format.base_format import BaseFormat


class CsvFormat(BaseFormat, ABC):
    @abstractmethod
    def get_csv_headers(self):
        raise NotImplementedError

    @abstractmethod
    def encode_to_csv(self) -> str:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def decode_from_csv(cls, csv: str) -> Self:
        raise NotImplementedError
