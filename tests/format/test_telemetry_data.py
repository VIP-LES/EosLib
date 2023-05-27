from EosLib.format.telemetry_data import TelemetryData


def get_good_telemetry_data():
    return TelemetryData(32.0,
                         1013.25,
                         50.5,
                         30.0,
                         45.0,
                         60.0)


def test_encode_decode_bytes():
    base_data = get_good_telemetry_data()
    encoded_new_data = base_data.encode()
    new_data = TelemetryData.decode(encoded_new_data)

    assert base_data.temperature == new_data.temperature \
           and base_data.pressure == new_data.pressure \
           and base_data.humidity == new_data.humidity \
           and base_data.x_rotation == new_data.x_rotation \
           and base_data.y_rotation == new_data.y_rotation \
           and base_data.z_rotation == new_data.z_rotation \
           and base_data.valid == new_data.valid


def test_encode_decode_csv():
    base_data = get_good_telemetry_data()
    encoded_new_data = base_data.encode()
    new_data = TelemetryData.decode(encoded_new_data)

    assert base_data.temperature == new_data.temperature \
           and base_data.pressure == new_data.pressure \
           and base_data.humidity == new_data.humidity \
           and base_data.x_rotation == new_data.x_rotation \
           and base_data.y_rotation == new_data.y_rotation \
           and base_data.z_rotation == new_data.z_rotation \
           and base_data.valid == new_data.valid
