
from datetime import datetime
from EosLib.format.position import Position, FlightState
import EosLib
from EosLib.packet import data_header, transmit_header
from EosLib.device import Device
from EosLib.packet import Packet
from EosLib.packet.definitions import Type


def test_position():
    """Tests encode and decode functions

    :returns: If encode and decode work
    :rtype: boolean
    """
    current_time = datetime.now()
    new_data = Position()

    # new_data.set_validity()
    time = current_time
    encoded_new_data = new_data.encode_position(time.timestamp(), 23.4, 23.4, 23.4, 23.4, 5,
                                                FlightState.NOT_SET)

    decoded_new_data = Position.decode_position(encoded_new_data)

    assert time == decoded_new_data.timestamp
    assert 23.4 == decoded_new_data.latitude
    assert 23.4 == decoded_new_data.longitude
    assert 23.4 == decoded_new_data.altitude
    assert 23.4 == decoded_new_data.speed
    assert 5 == decoded_new_data.number_of_satellites
    assert FlightState.NOT_SET == decoded_new_data.flight_state
    assert True == decoded_new_data.valid


def test_position_packet():

    position_data_header = EosLib.packet.data_header.DataHeader(Device.O3, Type.POSITION)
    position_transmit_header = EosLib.packet.transmit_header.TransmitHeader(2)

    current_time = datetime.now()
    new_data = Position()

    encoded_new_data = new_data.encode_position(current_time.timestamp(), 23.4, 23.4, 23.4, 23.4, 5,
                                                FlightState.NOT_SET)
    packet = Packet(encoded_new_data, position_data_header, position_transmit_header)

    decoded_new_data = Position.decode_position(packet)

    assert current_time == decoded_new_data.timestamp
    assert 23.4 == decoded_new_data.latitude
    assert 23.4 == decoded_new_data.longitude
    assert 23.4 == decoded_new_data.altitude
    assert 23.4 == decoded_new_data.speed
    assert 5 == decoded_new_data.number_of_satellites
    assert FlightState.NOT_SET == decoded_new_data.flight_state
    assert decoded_new_data.valid