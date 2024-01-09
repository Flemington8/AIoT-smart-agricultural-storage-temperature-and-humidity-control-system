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
    if command == 'fan_on & dehumidifier_on':
        command_fan_hex_str = '666F'
        command_dehumidifier_hex_str = '726F'
    elif command == 'fan_off & dehumidifier_off':
        command_fan_hex_str = '6666'
        command_dehumidifier_hex_str = '7266'
    elif command == 'fan_on & dehumidifier_off':
        command_fan_hex_str = '666F'
        command_dehumidifier_hex_str = '7266'
    else:
        command_fan_hex_str = '6666'
        command_dehumidifier_hex_str = '726F'

    try:
        command_fan_bytes = bytes.fromhex(command_fan_hex_str)  # convert hex string to bytes
        ser.write(command_fan_bytes)
        print("send fan command：", command_fan_bytes.decode('utf-8'))  # convert bytes to utf-8 string

        time.sleep(1)

        command_dehumidifier_bytes = bytes.fromhex(command_dehumidifier_hex_str)
        ser.write(command_dehumidifier_bytes)
        print("send dehumidifier command：", command_dehumidifier_bytes.decode('utf-8'))

    except Exception as e:
        print("error communicating in transmit...: " + str(e))

    finally:
        if command == 'fan_on & dehumidifier_on':
            return 'the fan has set on and the dehumidifier has set on.'
        elif command == 'fan_off & dehumidifier_off':
            return 'the fan has set off and the dehumidifier has set off.'
        elif command == 'fan_on & dehumidifier_off':
            return 'the fan has set on and the dehumidifier has set off.'
        else:
            return 'the fan has set off and the dehumidifier has set on.'


def receive_coordinator_data():
    try:
        while True:  # while ser.in_waiting: failed, because at first, ser.in_waiting is 0, so the while loop won't be executed.
            if ser.in_waiting:
                data_hex_str = ser.readline().hex()
                # read binary data from serial port & decode from binary to hex and restore it in a string
                # ser.readline() = {bytes: 12} b'!\x02\t\x00Z\x00*LV\x04\xe15'
                # ser.readline().hex() = {str} '210209005a002a4c5604e135'
                if data_hex_str[0:18] == '210209005a002b5458':  # '220209005a002a4c56':  # 02 is the light sensor's address
                    data_hex_chars_temp = data_hex_str[18:20]  # get the last two characters of the string
                    data_hex_chars_humidity = data_hex_str[20:22]
                    data_dec_chars_temp = int(data_hex_chars_temp, 16)
                    data_dec_chars_humidity = int(data_hex_chars_humidity, 16)
                    data_stack.put(data_dec_chars_humidity)
                    data_stack.put(data_dec_chars_temp)
                    # put data into the stack to share with other threads in order to ensure thread safety
                    print("receive temp：", 'decimal ', data_dec_chars_temp, 'hexadecimal ', data_hex_chars_temp)
                    print("receive humidity：", 'decimal ', data_dec_chars_humidity, 'hexadecimal ', data_hex_chars_humidity)
                    time.sleep(5)
    except Exception as e:
        print("error communicating in receive...: " + str(e))


thread = threading.Thread(target = receive_coordinator_data)
thread.start()
# You only call thread.join() in the main thread when it's necessary to gracefully shut down the program,
# ensuring that the background thread completes correctly and releases resources.
