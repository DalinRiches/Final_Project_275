# Using the pyserial library for serial communications


import serial
import datetime
import time



def delayMicroseconds(time):
    start = datetime.datetime.now()
    time_delta = datetime.timedelta(microseconds=time)

    while(True):
        now = datetime.datetime.now()
        if (now - start) >= time_delta:
            break
def sendbyte(serial, byte):
    serial.write(byte)

def logbyte(serial):
    value = serial.read()
    print(value)


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
                        default="/dev/ttyACM0")

    args = parser.parse_args()

    with serial.Serial() as ser:
        ser.baudrate = 115200;
        ser.port = "/dev/ttyACM0"

        ser.open()
        print("Trying to open: " + ser.port)


        while True:

            sendbyte(ser, 6)
            #Out of date pyserial we will need to update this
            if (ser.in_waiting > 0):
                logbyte(ser)

        ser.close()
