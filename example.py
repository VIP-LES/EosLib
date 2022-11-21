import datetime
import random

import EosLib.packet.definitions
import EosLib.packet.packet
import EosLib.packet.transmit_header

sequence_number = 0


# This makes some fake data, imagine it's a sensor or something
def collect_data() -> int:
    return random.randint(0, 100)


# This takes the data and generates a packet with a data header according to our needs
def log_data(data):
    data_header = EosLib.packet.packet.DataHeader(EosLib.Device.PRESSURE)
    data_header.data_type = EosLib.packet.definitions.Type.TELEMETRY
    data_header.priority = EosLib.packet.definitions.Priority.DATA
    data_header.sender = EosLib.packet.definitions.Device.PRESSURE
    data_header.generate_time = datetime.datetime.now()

    body = str(data)
    body = body.encode()

    created_packet = EosLib.packet.packet.Packet(body, data_header)

    with open("TestData.dat", 'w') as f:
        f.write(created_packet.encode_to_string())

    return created_packet


def transmit(sending_packet: EosLib.packet.packet.Packet):
    global sequence_number
    priority = sending_packet.data_header.priority
    # Manually handle the sequence number, but the date/time is automatically added
    new_transmit_header = EosLib.packet.transmit_header.TransmitHeader(sequence_number)
    sequence_number = (sequence_number + 1) % 256  # sequence number can't exceed 255, this makes sure that we don't

    sending_packet.transmit_header = new_transmit_header

    #  This packet is ready to be sent to the radio, however you're doing that would be handled here


if __name__ == "__main__":
    collected_data = collect_data()

    #  This is handled in the device driver, which will also send it to the radio
    data_packet = log_data(collected_data)

    #  The sequence number and transmit time should be set immediately before transmit
    #  So this really should happen on two threads, on to add it to the queue and one to grab it from the queue
    transmit(data_packet)
