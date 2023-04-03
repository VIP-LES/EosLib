from EosLib.device import Device
from EosLib.format.driver_health import DriverHealth, ThreadStatus
from EosLib.packet import Packet
from EosLib.packet.data_header import DataHeader
from EosLib.packet.definitions import Type


def test_driver_health():
    # this is dumb
    payload = DriverHealth(
        device_id=Device.NO_DEVICE,
        thread_count=1,
        read_thread_status=ThreadStatus.HEALTHY,
        command_thread_status=ThreadStatus.UNHEALTHY
    )
    header = DataHeader(
        sender=Device.ORCHEOSTRATOR,
        type=Type.DRIVER_HEALTH
    )
    packet = Packet.decode(Packet(data_header=header, body=payload.encode()).encode())
    assert payload == DriverHealth.decode(packet.body)
