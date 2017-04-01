
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
    serial.write(6)

def logbyte(serial):
    value = serial.read()
    print(value)


if __name__ == "__main__":
    # Code for processing route finding requests here

    wave_tables = wavetables.wavetable()
    oscil = osc.wtOsc(wave_tables=wave_tables.square())

    while (True):
        output = oscil.genOutput(["B", 4])
        print(output)
        time.sleep(0.000045351)
        #time.sleep(0.1)
