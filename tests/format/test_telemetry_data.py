# import EosLib

from datetime import datetime
from EosLib.format.telemetry_data import TelemetryData

"""Tests encode and decode functions

:returns: If encode and decode work
:rtype: boolean
"""
def test_telemetry_data():
    current_time = datetime.now().timestamp()
    new_data = TelemetryData(current_time, -40.3, 300, 50.5, 176.1, 196.5, 184.3)
    encoded_new_data = new_data.encode()
    decoded_new_data = TelemetryData.decode_data(encoded_new_data)

    assert new_data.timestamp == decoded_new_data.timestamp and new_data.temperature == decoded_new_data.temperature \
        and new_data.pressure == decoded_new_data.pressure and new_data.humidity == decoded_new_data.humidity \
            and new_data.x_rotation == decoded_new_data.x_rotation and new_data.y_rotation == decoded_new_data.y_rotation \
                and new_data.z_rotation == decoded_new_data.z_rotation and new_data.valid == decoded_new_data.valid
