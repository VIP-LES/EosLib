import io
import os

from EosLib.downlink.downlink_transmitter import DownlinkTransmitter
from EosLib.downlink.downlink_receiver import DownlinkReceiver
from EosLib.packet.packet import Packet, DataHeader, Priority
from EosLib.device import Device
from EosLib.format import Type

from EosLib.format.formats.downlink_chunk_format import DownlinkChunkFormat

if __name__ == "__main__":
    # Create a directory to store received chunks
    png_dir = "received_images"
    os.makedirs(png_dir, exist_ok=True)

    # reading file in binary mode
    with io.open("img.png", "rb") as downlink_file:
        transmitter = DownlinkTransmitter(downlink_file, 10)
        print(transmitter.num_chunks)
        # create a packet
        downlink_packet = Packet(transmitter.get_downlink_header(), DataHeader(Device.CAMERA_1,
                                                                               Type.DOWNLINK_COMMAND,
                                                                               Priority.DATA))
        # create the receiver
        receiver = DownlinkReceiver(downlink_packet, transmitter.get_downlink_header(), png_dir)

        # loops through all the chunks
        while (cur_chunk := transmitter.get_next_chunk()) is not None:
            print(cur_chunk.chunk_num)
            receiver.write_chunk(cur_chunk)

        # Send an ACK back to the transmitter
        ack_packet = receiver.get_ack()

        # If there are missing chunks in the ACK, retransmit them
        if ack_packet.missing_chunks:
            transmitter.retransmit_chunks(ack_packet.missing_chunks)
            # for chunk_num in ack_packet.missing_chunks:
            #     missing_chunk = transmitter.get_chunk(chunk_num)

        print(receiver.received_chunks)

