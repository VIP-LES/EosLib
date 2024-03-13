import csv
import io
import struct

from typing_extensions import Self

from EosLib.format.definitions import Type
from EosLib.format.csv_format import CsvFormat


class SystemHealthReport(CsvFormat):

    @staticmethod
    def get_format_type() -> Type:
        return Type.SYSTEM_HEALTH_REPORT

    @staticmethod
    def get_format_string() -> str:
        # Struct format is: cpu usage, cpu_temp, memory_usage, threads_in_use, num_drivers,
        #                   driver_states[] = device_id, state, last_updated
        return "!" \
               "f" \
               "f" \
               "f" \
               "d" \
               "d" \
               "d" \
               "d" \
               "d"

    def __init__(self,
                 cpu_usage: float,
                 cpu_temp: float,
                 memory_usage: float,
                 threads_in_use: int,
                 num_drivers: int,
                 device_id: int,
                 state: int,
                 last_updated: int):
        """Initializes data to parameters (default values otherwise)

        :param cpu_usage: The CPU usage, a percentage between 0 and 100
        :param cpu_temp: The CPU temperature in degrees Celsius
        :param memory_usage: The memory usage, a percentage between 0 and 100
        :param threads_in_use: The number of active threads
        :param num_drivers: The number of active drivers
        :param device_id: The id of the device we are querying
        :param state: The health status of the driver
        :param last_updated: The timestamp of the last update sent by the driver
        """
        self.cpu_usage = cpu_usage
        self.cpu_temp = cpu_temp
        self.memory_usage = memory_usage
        self.threads_in_use = threads_in_use
        self.num_drivers = num_drivers
        self.device_id = device_id
        self.state = state
        self.last_updated = last_updated
        self.valid = self.get_validity()

    def __eq__(self, other):
        return self.cpu_usage == other.cpu_usage and \
               self.cpu_temp == other.cpu_temp and \
               self.memory_usage == other.memory_usage and \
               self.threads_in_use == other.threads_in_use and \
               self.num_drivers == other.num_drivers and \
               self.device_id == other.device_id and \
               self.state == other.state and \
               self.last_updated == other.last_updated and \
               self.valid == other.valid

    def get_validity(self) -> bool:
        """Checks if data is valid

        Requirements:
        CPU Usage: Percentage between 0 and 100
        CPU Temp: Between 0 and 100 degrees Celsius
        Memory Usage: Percentage between 0 and 100
        Threads in Use: Greater than or equal to 0
        Number of Drivers: Greater than or equal to 0
        Device ID: Greater than or equal to 0
        Device State: Greater than or equal to 0
        Device Last Updated:
        """
        if self.cpu_usage is None or self.cpu_temp is None or self.memory_usage is None or \
           self.threads_in_use is None or self.num_drivers is None or self.device_id is None or \
           self.state is None or self.last_updated is None:
            return False
        elif self.cpu_usage < 0 or self.cpu_usage > 100 or \
                self.cpu_temp < 0 or self.cpu_temp > 100 or \
                self.memory_usage < 0 or self.memory_usage > 100 or \
                self.threads_in_use < 0 or \
                self.num_drivers < 0:
            return False
        else:
            return True

    def encode(self) -> bytes:
        return struct.pack(self.get_format_string(),
                           self.cpu_usage,
                           self.cpu_temp,
                           self.memory_usage,
                           self.threads_in_use,
                           self.num_drivers,
                           self.device_id,
                           self.state,
                           self.last_updated)

    @classmethod
    def decode(cls, data: bytes) -> Self:
        unpacked_data = struct.unpack(cls.get_format_string(), data)

        return SystemHealthReport(unpacked_data[0],
                                  unpacked_data[1],
                                  unpacked_data[2],
                                  unpacked_data[3],
                                  unpacked_data[4],
                                  unpacked_data[5],
                                  unpacked_data[6],
                                  unpacked_data[7])

    def get_csv_headers(self):
        return ["cpu_usage", "cpu_temp", "memory_usage", "threads_in_use", "num_drivers",
                "device_id", "state", "last_updated"]

    def encode_to_csv(self) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([str(self.cpu_usage),
                         str(self.cpu_temp),
                         str(self.memory_usage),
                         str(self.threads_in_use),
                         str(self.num_drivers),
                         str(self.device_id),
                         str(self.state),
                         str(self.last_updated)])

        return output.getvalue()

    @classmethod
    def decode_from_csv(cls, csv_string: str) -> Self:
        reader = csv.reader([csv_string])
        csv_list = list(reader)[0]

        return SystemHealthReport(float(csv_list[0]),
                                  float(csv_list[1]),
                                  float(csv_list[2]),
                                  int(csv_list[3]),
                                  int(csv_list[4]),
                                  int(csv_list[5]),
                                  int(csv_list[6]),
                                  int(csv_list[7]))
