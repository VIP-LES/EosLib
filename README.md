# EosLib

This is the Library for all code shared between the ground station and the payload in the Eos ecosystem.

Right now it contains the packet module, which allows for easy encoding and decoding of the packets used to communicate
between devices onboard the Eos payload, and between the Eos payload and the ground. It also contains the start of a
collection of data formats for efficient encoding/decoding. An overview of the packet format is given below.

## Installation

It is best to install EosLib via the requirements.txt files provided with both EosPayload and EosGround. If needed, it
can be installed directly via pip with `pip install git+https://github.com/VIP-LES/EosLib@main#egg=EosLib`, but this
introduces the possibility of version conflicts and should be a last resort.

## Further Documentation

To avoid this readme getting out of hand, there are separate readme files for the `packet` and `format` modules.
Real documentation is a work in progress.


## Using EosLib

Both `DataHeader` and `TransmitHeader` can be either created with their constructors, or be initialized as empty headers
and have data filled in at a later point. Once the requisite headers exist, a `Packet` can be initialized with those
headers as values in the constructor, or the `Packet` can be initialized as empty and have data provided at a later
point. Generally, it is better to use the constructor unless you have a compelling reason to do otherwise.

For an example, consult `test_packet.py`.
