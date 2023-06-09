import datetime

from EosLib.format.formats.position import Position
from EosLib.format.formats.position import FlightState

good_data_list = [datetime.datetime.now(),
                  33.7756,
                  84.3963,
                  974.5,
                  70.2,
                  5,
                  FlightState.DESCENT]


def get_position_from_list(position_list: [float]):
    return Position(position_list[0],
                    position_list[1],
                    position_list[2],
                    position_list[3],
                    position_list[4],
                    position_list[5],
                    position_list[6])


def get_good_position():
    return get_position_from_list(good_data_list)


def test_encode_decode_bytes():
    base_position = get_good_position()
    base_position_bytes = base_position.encode()
    new_position = Position.decode(base_position_bytes)
    assert base_position == new_position


def test_encode_decode_csv():
    base_position = get_good_position()
    base_position_csv = base_position.encode_to_csv()
    new_position = Position.decode_from_csv(base_position_csv)

    assert base_position == new_position


class TestEQ:
    def test_is_eq(self):
        data_1 = get_good_position()
        data_2 = get_good_position()

        assert data_1 == data_2

    def test_not_eq(self):
        test_passed = True

        data_1 = get_good_position()

        for i in range(len(good_data_list)):
            new_data_list = good_data_list
            if isinstance(good_data_list[i], float):
                new_data_list[i] += 1
            elif isinstance(good_data_list[i], datetime.datetime):
                new_data_list[i] += datetime.timedelta(1)
            elif isinstance(good_data_list[i], FlightState):
                new_data_list[i] = FlightState.ASCENT
            data_2 = get_position_from_list(new_data_list)

            if data_1 == data_2:
                test_passed = False

        assert test_passed

