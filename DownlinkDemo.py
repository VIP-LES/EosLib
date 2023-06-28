import io
import os

from EosLib.downlink.downlink_transmitter import DownlinkTransmitter
from EosLib.downlink.downlink_receiver import DownlinkReceiver
from EosLib.format.formats.downlink_chunk_format import DownlinkChunkFormat

if __name__ == "__main__":
    with io.open("img.png", "rb") as downlink_file:
        transmitter = DownlinkTransmitter(downlink_file, 10)
        print(transmitter.num_chunks)

        receiver = DownlinkReceiver(transmitter.get_downlink_header())

        with io.open("new_img.png", "ab") as new_downlink_file:
            for i in range(transmitter.num_chunks):
                print(transmitter.get_chunk(i))
                while (cur_chunk := transmitter.get_next_chunk()) is not None:
                    new_downlink_file.write(cur_chunk.chunk_body)
