import pytest

import EosLib

from datetime import datetime
from EosLib.format.TelemetryData import TelemetryData

def test_telemetry_data():
    current_time = datetime.now().timestamp()
    new_data = TelemetryData(current_time, 0, 0, 0, 0, 0, 0)
    valid = new_data.set_validity()
    encoded_new_data = new_data.encode_data()
    decoded_new_data = TelemetryData.decode_data(encoded_new_data)