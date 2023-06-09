from EosLib.format.formats.telemetry_data import TelemetryData


good_data_list = [32.0, 1013.25, 50.5, 30.0, 45.0, 60.0]


def get_telemetry_data_from_list(data_list: [float]):
    return TelemetryData(data_list[0],
                         data_list[1],
                         data_list[2],
                         data_list[3],
                         data_list[4],
                         data_list[5])


def get_good_telemetry_data():
    return get_telemetry_data_from_list(good_data_list)


def test_encode_decode_bytes():
    base_data = get_good_telemetry_data()
    encoded_new_data = base_data.encode()
    new_data = TelemetryData.decode(encoded_new_data)

    assert base_data == new_data


def test_encode_decode_csv():
    base_data = get_good_telemetry_data()
    encoded_new_data = base_data.encode()
    new_data = TelemetryData.decode(encoded_new_data)

    assert base_data == new_data


class TestEQ:
    def test_is_eq(self):
        data_1 = get_good_telemetry_data()
        data_2 = get_good_telemetry_data()

        assert data_1 == data_2

    def test_not_eq(self):
        test_passed = True

        data_1 = get_good_telemetry_data()

        for i in range(len(good_data_list)):
            new_data_list = good_data_list
            new_data_list[i] += 1
            data_2 = get_telemetry_data_from_list(new_data_list)

            if data_1 == data_2:
                test_passed = False

        assert test_passed

