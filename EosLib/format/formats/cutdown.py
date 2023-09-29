import csv
import io
import datetime
import struct
from typing_extensions import Self

from EosLib.format.definitions import Type
from EosLib.format.csv_format import CsvFormat


class CutDown(CsvFormat):

    @staticmethod
    def get_format_type() -> Type:
        return Type.COMMAND

    @staticmethod
    def get_format_string() -> str:
        # Struct format is: time, sender, packet_type, priority, destination, body
        return "!" \
               "d" \
               "d" \
               "d" \
               "d" \
               "d" \
               "d"

    def __init__(self,
                 time: datetime.datetime.now(),
                 sender: float = None,
                 packet_type: float = None,
                 priority: float = None,
                 destination: float = None,
                 body: float = None):
        """Initializes data to parameters (default values otherwise)

        :param temperature: The temperature data
        :param pressure: The pressure data
        :param humidity: The humidity data
        :param x_rotation: The x rotation data
        :param y_rotation: The y rotation data
        :param z_rotation: The z rotation data
        """
        self.time = time
        self.sender = sender
        self.packet_type = packet_type
        self.priority = priority
        self.destination = destination
        self.body = body
        self.valid = self.get_validity()

    def __eq__(self, other):
        return self.time == other.time and \
               self.sender == other.sender and \
               self.packet_type == other.packet_type and \
               self.priority == other.priority and \
               self.destination == other.destination and \
               self.body == other.body and \
               self.valid == other.valid

    def get_validity(self):
        """Checks if data is valid (NEED A MORE CONCRETE WAY OF VALIDATING)

        """
        if self.sender is None or self.destination is None or self.body is None:
            return False
        else:
            return True

    def encode(self) -> bytes:
        return struct.pack(self.get_format_string(),
                           self.time.timestamp(),
                           self.sender,
                           self.packet_type,
                           self.priority,
                           self.destination,
                           self.body)

    @classmethod
    def decode(cls, data: bytes) -> Self:
        unpacked_data = struct.unpack(cls.get_format_string(), data)

        return CutDown(datetime.datetime.fromtimestamp(unpacked_data[0]),
                       unpacked_data[1],
                       unpacked_data[2],
                       unpacked_data[3],
                       unpacked_data[4],
                       unpacked_data[5])

    def get_csv_headers(self):
        return ["time", "sender", "packet_type", "priority", "destination", "body"]

    def encode_to_csv(self) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([self.time.isoformat(),
                         str(self.sender),
                         str(self.packet_type),
                         str(self.priority),
                         str(self.destination),
                         str(self.body)])

        return output.getvalue()

    @classmethod
    def decode_from_csv(cls, csv_string: str) -> Self:
        reader = csv.reader([csv_string])
        csv_list = list(reader)[0]

        return CutDown(datetime.datetime.fromisoformat(csv_list[0]),
                       int(csv_list[1]),
                       int(csv_list[2]),
                       int(csv_list[3]),
                       int(csv_list[4]),
                       int(csv_list[5]))
