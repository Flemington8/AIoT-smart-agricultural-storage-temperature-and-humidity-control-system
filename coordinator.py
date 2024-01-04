import time

import serial

ser = serial.Serial(
    port = 'COM3',  # serial port
    baudrate = 115200,  # baud rate
    timeout = 1  # timeout in seconds
)
if ser.isOpen():
    print("Serial port is open.", ser.name)


def receive_coordinator_data():
    try:
        if ser.in_waiting:
            data = ser.readline().decode('utf-8').rstrip()
            print("receive：", data)
            return data

    except Exception as e:
        print("error communicating...: " + str(e))


def transmit_coordinator_data(data):
    try:
        hex_data = bytes.fromhex(data)
        ser.write(hex_data)
        print("send：", hex_data.hex())

    except Exception as e:
        print("error communicating...: " + str(e))
