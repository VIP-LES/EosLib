import definitions
import datetime


class Packet:
    def __init__(self, send_time: datetime.datetime = None, send_seq_num: int = None,
                 data_generate_time: datetime.datetime = None, data_packet_type: definitions.PacketType = None,
                 data_packet_sender: definitions.Device = None, data_packet_priority: definitions.Priority = None):
        self.send_time = send_time
        self.send_seq_num = send_seq_num
        self.data_generate_time = data_generate_time
        self.data_packet_type = data_packet_type
        self.data_packet_sender = data_packet_sender
        self.data_packet_priority = data_packet_priority

    # TODO: Implement this function
    def validate_transmit_header(self):
        pass

    # TODO: Implement this function
    def validate_data_header(self):
        pass

    # TODO: Implement this function
    def encode(self):
        pass


# TODO: Implement this function
def decode_packet():
    pass
