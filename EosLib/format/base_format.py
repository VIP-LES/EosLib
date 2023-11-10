import inspect
from abc import ABC
from abc import abstractmethod
from typing_extensions import Self

from EosLib.format.decode_factory import decode_factory
from EosLib.format.definitions import Type


class BaseFormat(ABC):
    def __init_subclass__(cls, **kwargs):
        if not inspect.isabstract(cls) or cls._i_promise_all_abstract_methods_are_implemented():
            decode_factory.register_decoder(cls)

    @staticmethod
    def _i_promise_all_abstract_methods_are_implemented() -> bool:
        """ This method exists because if you use a dataclass-based format ABC gets mad because it can't figure out
            that the dataclass implements __init__, __eq__, etc.

            :return: True if isabstract check should be bypassed, otherwise False
        """
        return False

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

    @abstractmethod
    def get_validity(self) -> bool:
        raise NotImplementedError
