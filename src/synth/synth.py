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

class synth:

    def __init__(self):
        self.time_delta = datetime.timedelta(microseconds=1)
        self.wave_tables = wavetables.wavetable()
        self.aud = alsaaudio.PCM()

        self.aud.setchannels(1)
        self.aud.setrate(16000) # 16000 Hz sample rate
        self.aud.setformat(alsaaudio.PCM_FORMAT_U8)
        self.audio_preload(self.aud)



        #ser =  serial.Serial(port='/dev/ttyACM5', baudrate=250000)



        # The period size controls the internal number of frames per period.
        # The significance of this parameter is documented in the ALSA api.
        self.aud.setperiodsize(255)

    def play(self, note=None, freq=None, time=0):
        oscil = osc.wtOsc(wave_tables=self.wave_tables.square())

        if not time:
            return
        self.time_delta2 = datetime.timedelta(seconds=time)
        starttime = datetime.datetime.now()
        now = datetime.datetime.now()
        if freq == None:
            if note == None:
                return
            while now - starttime < self.time_delta2:
                start = datetime.datetime.now()
                output = oscil.genOutput(note=note)

                self.aud.write(np.uint16(output))

                while(True):
                    now = datetime.datetime.now()
                    if (now - start) > self.time_delta:
                        break

        else:
            while now - starttime < self.time_delta2:
                start = datetime.datetime.now()
                output = oscil.genOutput(freq=freq)

                self.aud.write(np.uint16(output))

                while(True):
                    now = datetime.datetime.now()
                    if (now - start) > self.time_delta:
                        break



    def audio_preload(self, aud):

        for i in range(0,15000):
            aud.write(np.uint16(1))




'''
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
'''






if __name__ == "__main__":

    syn = synth();

    syn.play(note=['A',4],time=0.5)
    syn.play(note=['G',4],time=0.5)
    syn.play(note=['E',4],time=1)
    syn.play(note=['DS',4],time=0.5)
    syn.play(note=['B',5],time=0.5)
    syn.play(note=['FS',4],time=1)
    syn.play(freq=2000,time=3)

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
