import csv
import io
import struct
from typing_extensions import Self

from EosLib.format.definitions import Type
from EosLib.format.csv_format import CsvFormat


class EField(CsvFormat):

    @staticmethod
    def get_format_type() -> Type:
        return Type.E_FIELD

    @staticmethod
    def get_format_string() -> str:
        # Struct format is: voltage_a, voltage_b, voltage_c
        return "!" \
               "d" \
               "d" \
               "d"

    def __init__(self,
                 voltage_a: float,
                 voltage_b: float,
                 voltage_c: float):
        """Initializes data to parameters (default values otherwise)

        :param voltage_a: The temperature data
        :param voltage_b: The pressure data
        :param voltage_c: The humidity data
        """
        self.voltage_a = voltage_a
        self.voltage_b = voltage_b
        self.voltage_c = voltage_c
        self.valid = self.get_validity()

    def __eq__(self, other):
        return self.voltage_a == other.voltage_a and \
               self.voltage_b == other.voltage_b and \
               self.voltage_c == other.voltage_c and \
               self.valid == other.valid

    def get_validity(self) -> bool:
        """Checks if data is valid

        voltage range will be between 0-1.5 volts
        all 3 voltages need to be valid
        none of the voltages will be null
        """
        if self.voltage_a is None or self.voltage_b is None or self.voltage_c is None:
            return False
        elif self.voltage_a < 0 or self.voltage_a > 1.5 or \
                self.voltage_b < 0 or self.voltage_b > 1.5 or \
                self.voltage_c < 0 or self.voltage_c > 1.5:
            return False
        else:
            return True

    def encode(self) -> bytes:
        return struct.pack(self.get_format_string(),
                           self.voltage_a,
                           self.voltage_b,
                           self.voltage_c)

    @classmethod
    def decode(cls, data: bytes) -> Self:
        unpacked_data = struct.unpack(cls.get_format_string(), data)

        return EField(unpacked_data[0],
                      unpacked_data[1],
                      unpacked_data[2])

    def get_csv_headers(self):
        return ["voltage_a", "voltage_b", "voltage_c"]

    def encode_to_csv(self) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([str(self.voltage_a),
                         str(self.voltage_b),
                         str(self.voltage_c)])

        return output.getvalue()

    @classmethod
    def decode_from_csv(cls, csv_string: str) -> Self:
        reader = csv.reader([csv_string])
        csv_list = list(reader)[0]

        return EField(float(csv_list[0]),
                      float(csv_list[1]),
                      float(csv_list[2]))
