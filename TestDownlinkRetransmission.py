import io
import os
import time
import random

from EosLib.downlink.downlink_transmitter import DownlinkTransmitter
from EosLib.downlink.downlink_receiver import DownlinkReceiver
from EosLib.format.formats.downlink_chunk_format import DownlinkChunkFormat
from EosLib.packet.packet import Packet, DataHeader, Priority
from EosLib.device import Device
from EosLib.format import Type

# from EosLib.format.formats.downlink_chunk_format import DownlinkChunkFormat

if __name__ == "__main__":
    # Create a directory to store received chunks
    png_dir = "received_images"
    if not (os.path.exists(png_dir) and os.path.isdir(png_dir)):
        os.makedirs(png_dir, exist_ok=True)

    # reading file in binary mode
    with io.open("error.png", "rb") as downlink_file:
        transmitter = DownlinkTransmitter(downlink_file, 10)
        print(transmitter.num_chunks)
        # create a packet
        downlink_packet = Packet(transmitter.get_downlink_header(), DataHeader(Device.CAMERA_1,
                                                                               Type.DOWNLINK_COMMAND,
                                                                               Priority.DATA))
        # send packet to receiver
        receiver = DownlinkReceiver(downlink_packet, transmitter.get_downlink_header(), png_dir)

        def receive_chunks():
            # loops through all the chunks
            while (cur_chunk := transmitter.get_next_chunk()) is not None:
                # print(cur_chunk.chunk_body)

                # Simulate packet drops
                if random.random() >= 0.97:
                    receiver.write_chunk(cur_chunk)
                else:
                    print(f"Chunk {cur_chunk.chunk_num} has been dropped")

        # Get chunks for first time
        receive_chunks()

        # Get ack packet containing missing chunks from receiver
        ack_packet = receiver.get_ack()

        # If there are missing chunks in the ACK, retransmit them
        num_retransmits, max_transmits = 0, 10
        while ack_packet.missing_chunks and num_retransmits < max_transmits:
            print(f"Missing chunks: {ack_packet.missing_chunks}")
            transmitter.retransmit_chunks(ack_packet.missing_chunks)
            receive_chunks()
            time.sleep(0.1)
            ack_packet = receiver.get_ack()
            num_retransmits += 1

        if ack_packet.missing_chunks:
            print(f"Missing chunks {ack_packet.missing_chunks}, image is corrupted :/")

        print(f"Received Chunks: {receiver.received_chunks}")
