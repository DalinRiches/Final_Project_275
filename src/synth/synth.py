
import threading
import serial
import datetime
import time
import osc
import wavetables

#TODO: Clean this up into a class, this is a placeholder for testing
#      Make a communications class for serial, for the life of me i can't get pyserial to love me

def delayMicroseconds(time):
    start = datetime.datetime.now()
    time_delta = datetime.timedelta(microseconds=time)

    while(True):
        now = datetime.datetime.now()
        if (now - start) >= time_delta:
            break
def sendbyte(serial, byte):
    ser.write(bytes([byte]))

def logbyte(serial):
    value = serial.read()
    print(value)

if __name__ == "__main__":

    # 45 microsecond is ~22050 Hz
    dtime = 45;

    wave_tables = wavetables.wavetable()
    oscil = osc.wtOsc(wave_tables=wave_tables.square())
    time_delta = datetime.timedelta(microseconds=dtime)

    ser =  serial.Serial(port='/dev/ttyACM5', baudrate=250000)
    start = datetime.datetime.now()

    sT = threading.Thread(target = oscil.genOutput, args=(["A", 4]))
    oT = threading.Thread(target = sendbyte, args=(ser, output))
    oT =
    sT =

    while (True):

        #reads intial time


        output = oscil.genOutput(["A", 4])

        #waits until 45 microseconds have passed,
        now = datetime.datetime.now()
        while (now - start) < time_delta:
            now = datetime.datetime.now()
        print(now)
        ser.write(bytes([output]))

        start = datetime.datetime.now()

    ser.close()
