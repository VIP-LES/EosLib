# EosLib
This is the Library for all code shared between the ground station and the payload in the Eos ecosystem.

Right now it contains the packet module, which allows for easy encoding and decoding of the packets used to communicate 
between devices onboard the Eos payload, and between the Eos payload and the ground. An overview of the packet format is
given below.

## EosLib Packet Format

Each Packet is required to contain a `DataHeader`, which holds information about the source of the packet and 
information about what the body contains. Any Packet can also include a `TransmitHeader`, which holds information 
about the transmission of the packet, typically via radio.

### `DataHeader` Contents

| Field                | Variable Type           | Valid Range                  | Required? |
|----------------------|-------------------------|------------------------------|-----------|
| Packet Type          | PacketType enum         | Values in PacketType         | Yes       |
| Packet Sender        | PacketDevice enum       | Values in Device             | Yes       |
| Packet Priority      | PacketPriority enum\*\* | Values in PacketPriority\*\* | Yes       |
| Packet Generate Time | datetime                | Any valid date               | Yes\*     |


### `TransmitHeader` Contents

| Field                  | Variable Type | Valid Range    | Required? |
|------------------------|---------------|----------------|-----------|
| Packet Sequence Number | Int           | 0-255          | Yes       |
| Packet Timestamp       | datetime      | Any valid date | Yes\*     |

\* If no Timestamp is provided, a default value of `datetime.now()` is provided.

\*\* Packet Priority can be any integer value between 0-255, but sensible defaults are provided via the PacketPriority 
enum
