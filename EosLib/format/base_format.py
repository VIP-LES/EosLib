import inspect
from abc import ABC
from abc import abstractmethod
from typing_extensions import Self

from EosLib.format.decode_factory import decode_factory
from EosLib.format.definitions import Type


class BaseFormat(ABC):
    def __init_subclass__(cls, **kwargs):
        if not inspect.isabstract(cls):
            decode_factory.register_decoder(cls)

    @classmethod
    def get_decoders(cls) -> dict[type, callable]:
        return {bytes: cls.decode}

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_format_type() -> Type:
        raise NotImplementedError

    @abstractmethod
    def encode(self) -> bytes:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def decode(cls, data: bytes) -> Self:
        raise NotImplementedError
