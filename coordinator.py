import queue
import threading
import time

import serial

ser = serial.Serial(
    port = 'COM3',  # serial port
    baudrate = 115200,  # baud rate
    timeout = 1  # timeout in seconds
)
if ser.isOpen():
    print("Serial port {} is open.".format(ser.name))

data_stack = queue.LifoQueue()


def transmit_coordinator_command(command):
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


def transmit_coordinator_data():  # send data to coordinator temporarily
    try:
        data = '160'
        ser.write(data.encode('utf-8'))
    except Exception as e:
        print("error communicating in transmit data: " + str(e))


def receive_coordinator_data():
    try:
        while True:  # while ser.in_waiting: failed, because at first, ser.in_waiting is 0, so the while loop won't be executed.
            transmit_coordinator_data()  # send data to coordinator temporarily
            if ser.in_waiting:
                data = ser.readline().decode('utf-8').rstrip()  # read data from serial port until '\n' & decode from binary to utf-8
                data_stack.put(data)  # put data into the stack to share with other threads in order to ensure thread safety
                print("receive：", data)
            time.sleep(3)

    except Exception as e:
        print("error communicating in receive...: " + str(e))


thread = threading.Thread(target = receive_coordinator_data)
thread.start()
# You only call thread.join() in the main thread when it's necessary to gracefully shut down the program,
# ensuring that the background thread completes correctly and releases resources.
