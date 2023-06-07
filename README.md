# EosLib

This is the Library for all code shared between the ground station and the payload in the Eos ecosystem.

Right now it contains the packet module, which allows for easy encoding and decoding of the packets used to communicate
between devices onboard the Eos payload, and between the Eos payload and the ground. It also contains the start of a
collection of data formats for efficient encoding/decoding. An overview of the packet format is given below.

## Installation

It is best to install EosLib via the requirements.txt files provided with both EosPayload and EosGround. If needed, it
can be installed directly via pip with `pip install git+https://github.com/VIP-LES/EosLib@main#egg=EosLib`, but this
introduces the possibility of version conflicts and should be a last resort.

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
| Packet Destination   | PacketDevice enum       | Values in Device             | No        |
| Packet Generate Time | datetime                | Any valid date               | Yes\*     |

### `TransmitHeader` Contents

| Field                  | Variable Type | Valid Range    | Required? |
|------------------------|---------------|----------------|-----------|
| Packet Sequence Number | Int           | 0-255          | Yes       |
| Packet Timestamp       | datetime      | Any valid date | Yes\*     |

\* If no Timestamp is provided, a default value of `datetime.now()` is provided.

\*\* Packet Priority can be any integer value between 0-255, but sensible defaults are provided via the PacketPriority
enum. Unless you have good reason to provide your own value, use on of the options given in the enum.

## EosLib Data Formats

To avoid using strings in packet bodies, EosLib contains some pre-made data formats. Their contents are listed below.

### `Position` Format

| Field                | Variable Type    | Unit            |
|----------------------|------------------|-----------------|
| GPS Time             | datetime         | datetime        |
| Latitude             | float            | decimal degrees |
| Longitude            | float            | decimal degrees |
| Altitude             | float            | feet            |
| Speed                | float            | miles/hour      |
| Number of Satellites | int              | number          |
| Flight State         | FlightState enum | N/A             |

The `FlightState` enum contains 5 possible states, `NOT_SET`, `UNKNOWN`, `ON_GROUND`, `ASCENT`, and `DESCENT`. Their
use should be self-explanatory.

`Position` objects also automatically set a `valid` field when initialized or decoded. The logic is still pretty primitive, but it's a
good sanity check/first pass validity check.

### `Telemetry` Format

| Field       | Variable Type | Unit     |
|-------------|---------------|----------|
| Temperature | float         | celsius  |
| Pressure    | float         | mbar     |
| Humidity    | float         | %RH      |
| X-Rotation  | float         | degrees  |
| Y-Rotation  | float         | degrees  |
| Z-Rotation  | float         | degrees  |

Likewise to `Position` objects, `TelemetryData` objects automatically set a `valid` field when decoded. The current state it's in is quite surface level and will need a better system in the future.

## Using EosLib

Both `DataHeader` and `TransmitHeader` can be either created with their constructors, or be initialized as empty headers
and have data filled in at a later point. Once the requisite headers exist, a `Packet` can be initialized with those
headers as values in the constructor, or the `Packet` can be initialized as empty and have data provided at a later
point. Generally, it is better to use the constructor unless you have a compelling reason to do otherwise.

For an example, consult `test_packet.py`.
