# Using the pyserial library for serial communications
import sys
sys.path.insert(
    0, r'C:\Users\Dalin Riches\Desktop\School Files\Second Year\Sem 2\CMPUT275\Final Project\lib\textserial')

import serial
import datetime
import time
import cs_message
import textserial


def delayMicroseconds(time):
    start = datetime.datetime.now()
    time_delta = datetime.timedelta(microseconds=time)

    while(True):
        now = datetime.datetime.now()
        if (now - start) >= time_delta:
            break


if __name__ == "__main__":
    # Code for processing route finding requests here
    import argparse
    parser = argparse.ArgumentParser(
        description='Client-server message test.',
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("-d0",
                        help="Debug off",
                        action="store_false",
                        dest="debug")

    parser.add_argument("-s",
                        help="Set serial port for protocol",
                        nargs="?",
                        type=str,
                        dest="serial_port_name",
                        default="COM5")

    args = parser.parse_args()

    debug = args.debug

    set_logging(debug)

    import textserial
    serial_port_name = args.serial_port_name
    log_msg("Opening serial port: {}".format(serial_port_name))

    # Open up the connection
    baudrate = 115200  # [bit/seconds] 115200 also works

    with textserial.TextSerial(
            serial_port_name, baudrate, errors='ignore', timeout=None, newline=None) as ser:
        # Lines for test center or command line
        while True:
            for i in range(0, 255):
                line = receive_msg_from_client(ser)
                send_msg_to_client(ser, i)
