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


with serial.Serial() as ser:
    ser.baudrate = 9600
    ser.port = 'COM5'
    ser.open()

    # Wait five seconds for serial to init
    delayMicroseconds(5000000)

    x = 25

    while ser.is_open:
        ser.write(x)
        ser.write('\r\n'.encode('ascii'))
        ser.read
