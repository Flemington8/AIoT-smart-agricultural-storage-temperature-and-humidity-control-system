import queue
import threading

import serial

ser = serial.Serial(
    port = 'COM3',  # serial port
    baudrate = 115200,  # baud rate
    timeout = 1  # timeout in seconds
)
if ser.isOpen():
    print("Serial port {} is open.".format(ser.name))

data_queue = queue.Queue()


def transmit_coordinator_data(command):
    if command == 'ON':
        data = '01'
    else:
        data = '00'

    try:
        hex_data = bytes.fromhex(data)
        ser.write(hex_data)
        print("send：", hex_data.hex())

    except Exception as e:
        print("error communicating in transmit...: " + str(e))

    finally:
        if command == 'ON':
            return 'The lamp is turned on.'
        else:
            return 'The lamp is turned off.'


def receive_coordinator_data():
    try:
        while True:  # while ser.in_waiting: failed, because at first, ser.in_waiting is 0, so the while loop won't be executed.
            if ser.in_waiting:
                data = ser.readline().rstrip()  # read data from serial port until '\n'
                data_queue.put(data)
                print("receive：", data)

    except Exception as e:
        print("error communicating in receive...: " + str(e))


thread = threading.Thread(target = receive_coordinator_data)
thread.start()
