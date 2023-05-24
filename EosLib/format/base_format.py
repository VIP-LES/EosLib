from abc import ABC
from abc import abstractmethod
from typing_extensions import Self

import EosLib


class BaseFormat(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def encode(self) -> bytes:
        raise NotImplementedError

    def encode_for_transmit(self) -> bytes:
        return self.encode()[0:EosLib.packet.Packet.radio_body_max_bytes]

    @classmethod
    @abstractmethod
    def decode(cls, data: bytes | EosLib.packet.Packet) -> Self:
        raise NotImplementedError
