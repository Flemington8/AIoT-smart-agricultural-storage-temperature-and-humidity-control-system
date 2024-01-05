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
        data_hex_str = '6F'
    else:
        data_hex_str = '66'

    try:
        data_hex = bytes.fromhex(data_hex_str)
        ser.write(data_hex)
        print("send：", data_hex.hex())

    except Exception as e:
        print("error communicating in transmit...: " + str(e))

    finally:
        if command == 'ON':
            return 'the lamp has set on.'
        else:
            return 'the lamp has set off.'


def receive_coordinator_data():
    try:
        while True:  # while ser.in_waiting: failed, because at first, ser.in_waiting is 0, so the while loop won't be executed.
            if ser.in_waiting:
                data_hex_str = ser.readline().hex()
                # read binary data from serial port & decode from binary to hex and restore it in a string
                # ser.readline() = {bytes: 12} b'!\x02\t\x00Z\x00*LV\x04\xe15'
                # ser.readline().hex() = {str} '210209005a002a4c5604e135'
                if data_hex_str[2:4] == '02':  # 02 is the light sensor's address
                    data_hex_chars = data_hex_str[-6:-2]  # get the last two characters of the string
                    data_dec_chars = int(data_hex_chars, 16)
                    data_stack.put(data_dec_chars)
                    # put data into the stack to share with other threads in order to ensure thread safety
                    print("receive：", 'decimal-', data_dec_chars, 'hexadecimal-', data_hex_chars)
                    time.sleep(3)
    except Exception as e:
        print("error communicating in receive...: " + str(e))


thread = threading.Thread(target = receive_coordinator_data)
thread.start()
# You only call thread.join() in the main thread when it's necessary to gracefully shut down the program,
# ensuring that the background thread completes correctly and releases resources.
