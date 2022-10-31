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
    created_packet = EosLib.packet.packet.Packet()
    created_packet.data_header = EosLib.packet.packet.DataHeader()

    created_packet.data_header.data_packet_type = EosLib.packet.definitions.PacketType.TELEMETRY
    created_packet.data_header.data_packet_priority = EosLib.packet.definitions.PacketPriority.DATA
    created_packet.data_header.data_packet_sender = EosLib.packet.definitions.PacketDevice.ALTIMETER
    created_packet.data_header.data_packet_generate_time = datetime.datetime.now()

    created_packet.body = str(data)
    created_packet.body = created_packet.body.encode()

    with open("TestData.dat", 'wb') as f:
        f.write(created_packet.encode_packet())

    return created_packet


def transmit(sending_packet: EosLib.packet.packet.Packet):
    global sequence_number
    priority = sending_packet.data_header.data_packet_priority
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

