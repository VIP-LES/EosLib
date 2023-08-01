import io
import os

from EosLib.downlink.downlink_transmitter import DownlinkTransmitter
from EosLib.downlink.downlink_receiver import DownlinkReceiver
from EosLib.packet.packet import Packet, DataHeader, Priority
from EosLib.device import Device
from EosLib.format import Type

from EosLib.format.formats.downlink_chunk_format import DownlinkChunkFormat

if __name__ == "__main__":
    with io.open("img.png", "rb") as downlink_file:
        transmitter = DownlinkTransmitter(downlink_file, 10)
        print(transmitter.num_chunks)

        downlink_packet = Packet(transmitter.get_downlink_header(), DataHeader(Device.CAMERA_1,
                                                                               Type.DOWNLINK_COMMAND,
                                                                               Priority.DATA))

        receiver = DownlinkReceiver(downlink_packet, transmitter.get_downlink_header())

        while (cur_chunk := transmitter.get_next_chunk()) is not None:
            print(cur_chunk.chunk_body)
            receiver.write_chunk(cur_chunk)

