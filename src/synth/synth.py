import numpy as np
import serial
import osc
import wavetables
import alsaaudio
import math
import threading
import queue
import envolope


#TODO: Clean this up into a class, this is a placeholder for testing
#      Make a communications class for serial, for the life of me i can't get pyserial to love me

class synth:

    def __init__(self, volume=0.3):
        self.freqDict = self.gen_freq_table()
        self.samplerate = 44100
        self.ard_ex = False

        self.wave_tables = wavetables.wavetable(wav='Basic Shapes.wav', wtpos=1)
        self.wave_tables2 = wavetables.wavetable(wav='Basic Shapes.wav', wtpos=0)
        self.aud = alsaaudio.PCM(mode=alsaaudio.PCM_NONBLOCK)
        # Use these class objects to change the Oscillator setting's
        self.oscil = osc.wtOsc(self.freqDict,wave_tables=self.wave_tables.table, volume=0.3, detune=0,samplerate=self.samplerate)
        self.oscil2 = osc.wtOsc(self.freqDict,wave_tables=self.wave_tables.table, volume=0.75, detune=0, wavetablepos=0,samplerate=self.samplerate)
        self.env1 = envolope.envolope(self.samplerate,0.005,0,2)
        self.env2 = envolope.envolope(self.samplerate,0.005,0,2)
        self.volume = volume


        self.aud.setchannels(1)
        self.aud.setrate(self.samplerate) # 22050 Hz sample rate
        self.aud.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        #self.audio_preload(self.aud)



        #ser =  serial.Serial(port='/dev/ttyACM5', baudrate=250000)



        # The period size controls the internal number of frames per period.
        # The significance of this parameter is documented in the ALSA api.



    def gen_freq_table(self):
        tunefreq = 440
        a = 1.059463094359 # 2^(1/12)
        notes = {"C":-9,"B":2,"D":-7,"E":-5,"F":-4,"G":-2,"A":0,"CS":-8,"DS":-6,"FS":-3,"GS":-1,"AS":1}
        freqDic = {}

        def _getfreq_(semitonediff):
            freq = tunefreq * (pow(a, semitonediff))
            return freq

        def _getsemitonediff_f0_(note, octave):
            semitonediff = (octave-4)*12
            semitonediff = semitonediff + notes[note]
            return semitonediff

        for i in range(0,11):
            for l in notes.keys():
                semitonedif = _getsemitonediff_f0_(l, i)
                freq = _getfreq_(semitonedif)
                freqDic[l+' {}'.format(i)] = freq

        return freqDic



    def play(self, sequence, slide=False):

        totaltime = 0

        totalsamples = 0
        samples = []

        for i in sequence:
            numsamples = i[1] * self.samplerate
            totalsamples += numsamples
            notesamp =[]
            if not slide:
                self.oscil.phasor = 0
                self.oscil2.phasor = 0

            freq = self.freqDict[i[0]]

            count = 0
            while count < numsamples:
                # This is the order the synth will run

                # Run oscs
                sig1 = self.oscil.genOutput(freq)
                sig2 = self.oscil2.genOutput(freq)

                if sig1 > 32768:
                    sig1 = 32768 - sig1
                if sig1 > 32768:
                    sig1 = 32768 - sig1

                # Feed into envolope
                sig1 = sig1*self.env1.gen_env(count)
                sig2 = sig2*self.env2.gen_env(count)

                #mixes the two


                output = ((sig1 + sig2)//2)*self.volume
                notesamp.append(output)
                count += 1

            samples.append(notesamp)

        self.aud.setperiodsize(totalsamples*2)

        for i in samples:
            self.aud.write(np.int16(i))




    def audio_preload(self, aud):
        aud.paus(True)
        for i in range(0,32000):
            aud.write(np.uint16(1))
        aud.pause(False)



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
    sequence = [['A 3',2],['G 3',2],['F 3',2],['D 4',2],['C 4',2]]

    syn.play(sequence)


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
