import csv
import io
import struct
from typing_extensions import Self

from EosLib.format.definitions import Type
from EosLib.format.csv_format import CsvFormat


class FieldMill(CsvFormat):
    # Placeholder values for max and min values
    # Replace with correct values for validity check
    MAX_FREQUENCY = 999.9
    MIN_FREQUENCY = 0.0
    MAX_VOLTAGE = 999.9
    MIN_VOLTAGE = 0.0

    @staticmethod
    def get_format_type() -> Type:
        return Type.FIELDMILL

    @staticmethod
    def get_format_string() -> str:
        # Struct format is: frequency, voltage
        return "!" \
               "d" \
               "d"

    def __init__(self,
                 frequency: float,
                 voltage: float):
        """Initializes data to parameters (default values otherwise)

        :param frequency: The frequency data
        :param voltage: The voltage data
        """
        self.frequency = frequency
        self.voltage = voltage
        self.valid = self.get_validity()

    def __eq__(self, other):
        return self.frequency == other.frequency and \
            self.voltage == other.voltage and \
            self.valid == other.valid

    def get_validity(self) -> bool:
        """Checks if data is valid
        frequency range will be determined
        voltage range will be determined
        frequency and voltage need to be valid
        none of the values will be null
        """
        if self.frequency is None or self.voltage is None:
            return False
        elif self.frequency < self.MIN_FREQUENCY or self.frequency > self.MAX_FREQUENCY or \
                self.voltage < self.MIN_VOLTAGE or self.voltage > self.MAX_VOLTAGE:
            return False
        else:
            return True

    def encode(self) -> bytes:
        return struct.pack(self.get_format_string(),
                           self.frequency,
                           self.voltage)

    @classmethod
    def decode(cls, data: bytes) -> Self:
        unpacked_data = struct.unpack(cls.get_format_string(), data)
        return FieldMill(unpacked_data[0],
                         unpacked_data[1])

    def get_csv_headers(self):
        return ["frequency", "voltage"]

    def encode_to_csv(self) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([str(self.frequency),
                         str(self.voltage)])
        return output.getvalue()

    @classmethod
    def decode_from_csv(cls, csv_string: str) -> Self:
        reader = csv.reader([csv_string])
        csv_list = list(reader)[0]

        return FieldMill(float(csv_list[0]),
                      float(csv_list[1]))
