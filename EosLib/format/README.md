# EosLib Formats

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

### `CutDown` Format

| Field | Variable Type | Unit |
|-------|---------------|------|
| Ack   | unsigned char | N/A  |

`Ack` is an acknowledgement for the payload receiving our command, incrementing for each command sent. The payload should echo `Ack` back to the ground station if the command is received.
