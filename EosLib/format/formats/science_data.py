from dataclasses import dataclass, field
from datetime import datetime
import csv
import io
import struct
from typing_extensions import Self

from EosLib.format.definitions import Type
from EosLib.format.csv_format import CsvFormat


@dataclass
class ScienceData(CsvFormat):
    """
    This is the format for representing the output of the science sensors driver.
    Turns out it's chonk, ~104 bytes.  If more fields are added, maybe consider breaking up the packets so we don't
    hit radio max bytes
    """

    # note: all _count variables are unitless.  Some things can be calculated by referencing the data
    #       sheets though.  But otherwise consider it a relative measure of comparison.
    temperature_celsius: float         # from SHTC3 temperature-humidity sensor        (double)
    relative_humidity_percent: float   # from SHTC3 temperature-humidity sensor        (double)
    temperature_celsius_2: float       # from BMP388 temperature-pressure sensor       (double)
    pressure_hpa: float                # from BMP388 temperature-pressure sensor       (double)
    altitude_meters: float             # from BMP388 temperature-pressure sensor       (double)
    ambient_light_count: int           # from LTR390 uv-light sensor                   (uint?)
    ambient_light_lux: float           # from LTR390 uv-light sensor                   (double)
    uv_count: int                      # from LTR390 uv-light sensor                   (uint?)
    uv_index: float                    # from LTR390 uv-light sensor                   (double)
    infrared_count: int                # from TSL2591 ir-light sensor                  (ushort)
    visible_count: int                 # from TSL2591 ir-light sensor                  (uint)
    full_spectrum_count: int           # from TSL2591 ir-light sensor                  (uint)
    ir_visible_lux: float              # from TSL2591 ir-light sensor                  (double)
    pm10_standard_ug_m3: int           # from PMSA003I particulate sensor              (ushort)
    pm25_standard_ug_m3: int           # from PMSA003I particulate sensor              (ushort)
    pm100_standard_ug_m3: int          # from PMSA003I particulate sensor              (ushort)
    pm10_environmental_ug_m3: int      # from PMSA003I particulate sensor              (ushort)
    pm25_environmental_ug_m3: int      # from PMSA003I particulate sensor              (ushort)
    pm100_environmental_ug_m3: int     # from PMSA003I particulate sensor              (ushort)
    particulate_03um_per_01L: int      # from PMSA003I particulate sensor              (ushort)
    particulate_05um_per_01L: int      # from PMSA003I particulate sensor              (ushort)
    particulate_10um_per_01L: int      # from PMSA003I particulate sensor              (ushort)
    particulate_25um_per_01L: int      # from PMSA003I particulate sensor              (ushort)
    particulate_50um_per_01L: int      # from PMSA003I particulate sensor              (ushort)
    particulate_100um_per_01L: int     # from PMSA003I particulate sensor              (ushort)

    # useful for csv, not included in binary encode/decode, use data header instead.  Not compared in __eq__
    timestamp: datetime | None = field(default=None, compare=False)

    @staticmethod
    def _i_promise_all_abstract_methods_are_implemented() -> bool:
        return True

    @staticmethod
    def get_format_type() -> Type:
        return Type.SCIENCE_DATA

    @staticmethod
    def get_format_string() -> str:
        #         SHTC3 BMP388 LTR390 TSL2591 PMSA003I = 104 bytes
        return "!  2d     3d    IdId   HIId     12H   "

    def get_csv_headers(self):
        return [
            'timestamp', 'temperature_celsius', 'relative_humidity_percent', 'temperature_celsius_2', 'pressure_hpa',
            'altitude_meters', 'ambient_light_count', 'ambient_light_lux', 'uv_count', 'uv_index', 'infrared_count',
            'visible_count', 'full_spectrum_count', 'ir_visible_lux', 'pm10_standard_ug_m3', 'pm25_standard_ug_m3',
            'pm100_standard_ug_m3', 'pm10_environmental_ug_m3', 'pm25_environmental_ug_m3', 'pm100_environmental_ug_m3',
            'particulate_03um_per_01L', 'particulate_05um_per_01L', 'particulate_10um_per_01L',
            'particulate_25um_per_01L', 'particulate_50um_per_01L', 'particulate_100um_per_01L'
        ]

    def encode(self) -> bytes:
        return struct.pack(
            self.get_format_string(),
            self.temperature_celsius,
            self.relative_humidity_percent,
            self.temperature_celsius_2,
            self.pressure_hpa,
            self.altitude_meters,
            self.ambient_light_count,
            self.ambient_light_lux,
            self.uv_count,
            self.uv_index,
            self.infrared_count,
            self.visible_count,
            self.full_spectrum_count,
            self.ir_visible_lux,
            self.pm10_standard_ug_m3,
            self.pm25_standard_ug_m3,
            self.pm100_standard_ug_m3,
            self.pm10_environmental_ug_m3,
            self.pm25_environmental_ug_m3,
            self.pm100_environmental_ug_m3,
            self.particulate_03um_per_01L,
            self.particulate_05um_per_01L,
            self.particulate_10um_per_01L,
            self.particulate_25um_per_01L,
            self.particulate_50um_per_01L,
            self.particulate_100um_per_01L,
        )

    @classmethod
    def decode(cls, data: bytes) -> Self:
        unpacked_data = struct.unpack(cls.get_format_string(), data)
        return ScienceData(*unpacked_data)

    def encode_to_csv(self) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            self.timestamp.isoformat() if self.timestamp is not None else None,
            str(self.temperature_celsius),
            str(self.relative_humidity_percent),
            str(self.temperature_celsius_2),
            str(self.pressure_hpa),
            str(self.altitude_meters),
            str(self.ambient_light_count),
            str(self.ambient_light_lux),
            str(self.uv_count),
            str(self.uv_index),
            str(self.infrared_count),
            str(self.visible_count),
            str(self.full_spectrum_count),
            str(self.ir_visible_lux),
            str(self.pm10_standard_ug_m3),
            str(self.pm25_standard_ug_m3),
            str(self.pm100_standard_ug_m3),
            str(self.pm10_environmental_ug_m3),
            str(self.pm25_environmental_ug_m3),
            str(self.pm100_environmental_ug_m3),
            str(self.particulate_03um_per_01L),
            str(self.particulate_05um_per_01L),
            str(self.particulate_10um_per_01L),
            str(self.particulate_25um_per_01L),
            str(self.particulate_50um_per_01L),
            str(self.particulate_100um_per_01L),
        ])

        return output.getvalue()

    @classmethod
    def decode_from_csv(cls, csv_string: str) -> Self:
        reader = csv.reader([csv_string])
        csv_list = list(reader)[0]
        ret = ScienceData(
            float(csv_list[1]),
            float(csv_list[2]),
            float(csv_list[3]),
            float(csv_list[4]),
            float(csv_list[5]),
            int(csv_list[6]),
            float(csv_list[7]),
            int(csv_list[8]),
            float(csv_list[9]),
            int(csv_list[10]),
            int(csv_list[11]),
            int(csv_list[12]),
            float(csv_list[13]),
            int(csv_list[14]),
            int(csv_list[15]),
            int(csv_list[16]),
            int(csv_list[17]),
            int(csv_list[18]),
            int(csv_list[19]),
            int(csv_list[20]),
            int(csv_list[21]),
            int(csv_list[22]),
            int(csv_list[23]),
            int(csv_list[24]),
            int(csv_list[25]),
            datetime.fromisoformat(csv_list[0]) if csv_list[0] is not None else None
        )
        return ret
