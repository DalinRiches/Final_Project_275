import numpy as np
import serial
import datetime
import time
import osc
import wavetables
import alsaaudio
import threading

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


def audio_preload(aud):

    for i in range(0,3600):
        aud.write(np.uint16(1))




if __name__ == "__main__":
    # Code for processing route finding requests here
    time_delta = datetime.timedelta(microseconds=30)
    time_delta2 = datetime.timedelta(seconds=1)

    wave_tables = wavetables.wavetable()
    oscil = osc.wtOsc(wave_tables=wave_tables.square())

    #ser =  serial.Serial(port='/dev/ttyACM5', baudrate=250000)

    aud = alsaaudio.PCM()

    aud.setchannels(1)
    aud.setrate(16000) # 16000 Hz sample rate
    aud.setformat(alsaaudio.PCM_FORMAT_U8)

    # The period size controls the internal number of frames per period.
    # The significance of this parameter is documented in the ALSA api.
    aud.setperiodsize(260)

    audio_preload(aud)
    while True:
        for i in [['A',5],['B',5],['C',5]]:
            actualstart=datetime.datetime.now()
            while (True):
                start = datetime.datetime.now()
                output = oscil.genOutput(i)
                aud.write(np.uint16(output))




                while(True):
                    now = datetime.datetime.now()
                    if (now - start) > time_delta:
                        break

                if (now - actualstart) > time_delta2:
                    break
    '''
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
    '''
