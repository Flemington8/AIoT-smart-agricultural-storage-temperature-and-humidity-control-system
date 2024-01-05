# ChatGPT Smart Home Assistant

## Description

This project uses the ChatGPT API to create a smart home assistant that interacts with home appliances through a serial port.
The system can control home lighting and fans based on environmental parameters, such as brightness, temperature.
It's a Python-based project that uses serial communication to control the IoT devices.

## Installation

### prerequisites

Python 3.11 or higher

### Install the required packages

conda install pyserial==3.5
pip install serial==0.0.97
pip install openai==1.6.1
Usage
Install the required Python libraries and configure settings for OpenAI and serial communication.
Run the scripts, which will continuously monitor environmental parameters and interact with the OpenAI API for control instructions.
python OpenAI_Assistant_API.py
or
python OpenAI_Chat_Completion_API.py
The OpenAI_Assistant_API.py is more advanced and can handle multiple commands in a single request.
The scripts control the corresponding home appliances based on instructions received from the OpenAI API.


Note: Ensure the OpenAI API key is correctly configured.
Make sure the serial communication settings are correct, and the relevant hardware devices are connected.