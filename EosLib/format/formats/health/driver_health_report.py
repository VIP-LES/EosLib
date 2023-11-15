from dataclasses import dataclass
from enum import IntEnum, unique
from typing_extensions import Self
import struct

from EosLib.format.base_format import BaseFormat
from EosLib.format.definitions import Type

@unique
class ThreadStatus(IntEnum):
    NONE = 0
    INVALID = 1
    REGISTERED = 2
    ALIVE = 3
    DEAD = 4


@dataclass
class DriverHealthReport(BaseFormat):

    is_healthy:              bool       # true if healthy                                                (bool)
    custom_state_bitvector:  int        # may be used by the driver for any custom purpose               (uchar)
    num_threads:             int        # of threads, including main and mqtt (uchar)
    thread_statuses:         list[int]  # list of ThreadStatuses of size num_threads - 1, starting with  (uchar[])
                                        # mqtt and then registered threads in order of registration

    @staticmethod
    def _i_promise_all_abstract_methods_are_implemented() -> bool:
        return True

    @staticmethod
    def get_format_type() -> Type:
        return Type.DRIVER_HEALTH_REPORT

    def get_validity(self) -> bool:
        thread_status_bounds_all_good = True
        for thread_status in self.thread_statuses:
            try:
                ThreadStatus(thread_status)
            except ValueError:
                thread_status_bounds_all_good = False
                break

        return (
            0 <= self.custom_state_bitvector <= 255
            and 2 <= self.num_threads <= 63  # there is some maximum much less than 255, so just giving a guess
            and len(self.thread_statuses) == self.num_threads - 1
            and thread_status_bounds_all_good
        )

    def encode(self) -> bytes:
        format_string = "?BB" + "B"*(self.num_threads - 1)
        return struct.pack(
            format_string,
            self.is_healthy,
            self.custom_state_bitvector,
            self.num_threads,
            *self.thread_statuses,
        )

    @classmethod
    def decode(cls, data: bytes) -> Self:
        # start with the fields that will always be present (is_healthy, custom_bitvector, num_threads)
        constant_part_format_string = "?BB"
        offset = struct.calcsize(constant_part_format_string)
        is_healthy, custom_state_bitvector, num_threads = struct.unpack(constant_part_format_string, data[:offset])

        # now do the thread_status_array which is variable-length (depends on num_threads)
        if not (2 <= num_threads <= 63):
            raise ValueError(f"Failed to decode: num_threads must between 2 and 63, got {num_threads}")
        thread_statuses_format_string = "B"*(num_threads - 1)
        thread_statuses: list[int] = list(struct.unpack(thread_statuses_format_string, data[offset:]))
        return DriverHealthReport(is_healthy, custom_state_bitvector, num_threads, thread_statuses)


