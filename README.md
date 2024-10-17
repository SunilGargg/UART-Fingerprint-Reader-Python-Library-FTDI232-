# UART Fingerprint Reader Python Library (FTDI232)

A Python library for interfacing with the UART Fingerprint Reader module using an FTDI232 adapter.

## Device Information

This repository provides a Python library to interface with the [Waveshare UART Fingerprint Reader module](http://www.waveshare.com/uart-fingerprint-reader.htm) using the FTDI232 module to communicate over UART.

## Features

- **Connect using FTDI232**: This library communicates with the fingerprint sensor via UART using FTDI232 for reliable communication.
- **Python-based interface**: Easily control and interact with the fingerprint reader directly from Python code.
- **Supports various fingerprint operations**: Enroll, search, delete, and manage fingerprints stored on the device.
- **Works with multiple fingerprint matching modes**: 1:1 and 1:N.

## Manual
![image](https://github.com/user-attachments/assets/29706605-b59a-4a2b-8c4f-1094f990816b)

Please refer to the [official manual](http://www.waveshare.com/uart-fingerprint-reader.htm) for more detailed technical information and usage instructions for the UART fingerprint reader.

## Product Specifications

| Parameter                | Specification                |
|--------------------------|------------------------------|
| **Processor (CPU)**       | STM32F205                    |
| **Sensor**                | HD optical                   |
| **Memory**                | Built-in (extensible)        |
| **Anti-wearing**          | 1 million times              |
| **Anti-electrostatic**    | 150KV                        |
| **Fingerprint capacity**  | 1000                         |
| **False acceptance rate** | <0.001% (on security level 5)|
| **False rejection rate**  | <0.1% (on security level 5)  |
| **Current**               | <50mA                        |
| **Input time**            | <0.5s                        |
| **Matching time**         | <0.5s                        |
| **Matching mode**         | 1:1, 1:N                     |
| **Security level**        | 1-10 (supports customization)|
| **Output formats**        | User ID, Image, Feature      |
| **Feature size**          | 196 Bytes                    |
| **Feature template size** | 512 Bytes                    |
| **Template rule standard**| ISO19794-2                   |
| **Communication interface** | UART                      |
| **Communication baud rate** | 9600-57600bps              |
| **Power supply**          | UART, external power         |
| **Voltage level**         | 3.3-7.5V                     |
| **PCB dimensions**        | 40 x 58 x 8 mm               |
| **Operating temperature** | -20℃ to 60℃                 |
| **Relative humidity**     | 40%RH to 85%RH (without condensation)|

## Prerequisites

### Hardware

- [Waveshare UART Fingerprint Reader](http://www.waveshare.com/uart-fingerprint-reader.htm)
- FTDI232 module for UART communication
- Jumper wires for connecting the FTDI232 module to the fingerprint reader

### Software

- Python 3.x
- Required Python packages (you can install these using `pip`):
    - `pyserial`
    - Any other dependencies specific to your code

**Connect the hardware**:
   - Connect the FTDI232 module to the UART fingerprint reader module:
     - FTDI232 TX → Fingerprint Reader RX
     - FTDI232 RX → Fingerprint Reader TX
     - GND → GND
     - 5V/3.3V → VCC (Check the power requirements for your specific setup)

## Usage

The Python library provides functions for basic operations with the fingerprint reader, including:

- **Enroll fingerprint**: Save a new fingerprint template on the device.
- **Search fingerprint**: Search for a fingerprint match.
- **Delete fingerprint**: Remove a specific fingerprint from the device.
- **Clear all fingerprints**: Remove all fingerprints stored on the device.
  
---

This `README.md` template will serve as an effective introduction to your project, explaining the key components and usage details to potential contributors or users. Let me know if you need more specific details or if there's anything else you want to add!
