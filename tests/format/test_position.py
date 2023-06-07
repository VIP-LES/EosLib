import datetime

from EosLib.format.formats.position import Position
from EosLib.format.formats.position import FlightState


def get_good_position():
    return Position(datetime.datetime.now(),
                    33.7756,
                    84.3963,
                    974.5,
                    70.2,
                    5,
                    FlightState.DESCENT)


def test_encode_decode_bytes():
    base_position = get_good_position()
    base_position_bytes = base_position.encode()
    new_position = Position.decode(base_position_bytes)
    assert base_position.gps_time == new_position.gps_time and \
           base_position.latitude == new_position.latitude and \
           base_position.longitude == new_position.longitude and \
           base_position.altitude == new_position.altitude and \
           base_position.speed == new_position.speed and \
           base_position.number_of_satellites == new_position.number_of_satellites and \
           base_position.flight_state == new_position.flight_state


def test_encode_decode_csv():
    base_position = get_good_position()
    base_position_csv = base_position.encode_to_csv()
    new_position = Position.decode_from_csv(base_position_csv)

    assert base_position.gps_time == new_position.gps_time and \
           base_position.latitude == new_position.latitude and \
           base_position.longitude == new_position.longitude and \
           base_position.altitude == new_position.altitude and \
           base_position.speed == new_position.speed and \
           base_position.number_of_satellites == new_position.number_of_satellites and \
           base_position.flight_state == new_position.flight_state
