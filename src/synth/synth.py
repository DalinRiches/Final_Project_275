import numpy as np
import serial
import osc
import wavetables
import alsaaudio
import math
import envelope


class synth:
    '''
        This class is the main combined synthesizor this will generate audio
        from the speakers, in the future downloading to arduino for playback
        will be supported.

        Contains:
            -Two oscilator's    (Implemented)
            -An envelope for each oscillator    (Implemented)
            -A single filter both streams get combined then passed through    (Not Implemented)
            -A single delay the filtered stream is passed through    (Might Implemente)
            -Three LFO's for modulation of parameter's   (Not implemented)

        Controlling these is simple as each of their objects are created when a synth class
        is created.

        Audio playback takes a sequence from the sequencer, which will probably be made in the gui stuff.
        It then generates the audio for the entire sequence and plays it back through the speaker.
        If set to upload to arduino it does not output to speakers and converts the bitstream from
        PCM_FORMAT_S16_LE to uint8_t which the arduino downloads and plays on reset

            Args:
                volume=1    float, scaling factor for final audio stream amplitude

            Returns:
                None
    '''

    def __init__(self, volume=1):
        self.samplerate = 44100
        self.ard_ex = False

        self.wave_tables = wavetables.wavetable(wav='Basic Shapes.wav')
        self.wave_tables2 = wavetables.wavetable(wav='Basic Shapes.wav')
        self.aud = alsaaudio.PCM(mode=alsaaudio.PCM_NONBLOCK)
        # Use these class objects to change the Oscillator setting's
        self.oscil = osc.wtOsc(wave_tables=self.wave_tables.table, volume=0.75, detune=0, wavetablepos=0, samplerate=self.samplerate)
        self.oscil2 = osc.wtOsc(wave_tables=self.wave_tables.table, volume=0.75, detune=0, wavetablepos=6, samplerate=self.samplerate)
        self.env1 = envelope.envelope(self.samplerate,0.019,1,0.2)
        self.env2 = envelope.envelope(self.samplerate,0.019,1,2)
        self.volume = volume


        self.aud.setchannels(1)
        self.aud.setrate(self.samplerate) # 22050 Hz sample rate
        self.aud.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        #self.audio_preload(self.aud)



        #ser =  serial.Serial(port='/dev/ttyACM5', baudrate=250000)



        # The period size controls the internal number of frames per period.
        # The significance of this parameter is documented in the ALSA api.



    def gen_freq(self, note, osc):
        '''
            This function takes the note and detune from an wtosc object and gives
            the frequency

                Args:
                    note    list, containing two elements the string for the note, and the octave.
                                Ex. ['A', 4] = A from the fourth octave
                                Ex. ['FS', 5] = F sharp from the fifth octave

                    osc     wtosc, Uses to grab the proper detune.

                Returns:
                    float, corresponding to the frequency
        '''

        tunefreq = 440
        a = 1.059463094359 # 2^(1/12)
        notes = {"C":-9,"B":2,"D":-7,"E":-5,"F":-4,"G":-2,"A":0,"CS":-8,"DS":-6,"FS":-3,"GS":-1,"AS":1}


        def _getfreq_(semitonediff):
            freq = tunefreq * (pow(a, semitonediff))
            return freq

        def _getsemitonediff_f0_(note, octave):
            semitonediff = (octave-5)*12
            semitonediff = semitonediff + notes[note]
            return semitonediff


        semitonedif = _getsemitonediff_f0_(note[0], note[1]) + osc.detune
        freq = _getfreq_(semitonedif)
        return freq



    def play(self, sequence, slide=False, ard_rec=False):
        '''
            This function takes a squence and generates and plays the audio for that sequence.

                Args:
                    sequence    list, containing a note ( ['note',octave] ) and the time
                                (float corresponding to seconds) it's played
                                    Ex. [['A',4],4] = Play A 4 for 4 seconds

                    slide=False     bool, if True don't reset osc's phasor after each note
                                    if False, reset the phasor after each note

                    ard_rec=False   bool, if True record and upload to arduino
                                    if, False record and play through speakers

                Returns:
                    None
        '''

        totaltime = 0

        totalsamples = 0
        samples = []

        for i in sequence:
            numsamples = i[1] * self.samplerate
            totalsamples += math.floor(numsamples)
            notesamp =[]
            if not slide:
                self.oscil.phasor = 0
                self.oscil2.phasor = 0

            freq1 = self.gen_freq(i[0], self.oscil)
            freq2 = self.gen_freq(i[0], self.oscil2)

            count = 0
            while count < numsamples:
                # This is the order the synth will run

                # Run oscs
                sig1 = self.oscil.genOutput(freq1)
                sig2 = self.oscil2.genOutput(freq2)


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



if __name__ == "__main__":

    syn = synth();
    sequence = [[['A',4],4],[['G',4],2],[['F',4],2],[['A',4],0.5],[['G',4],0.5],[['F',4],0.5],[['A',4],0.5],
                    [['G',4],1],[['F',4],1]]

    syn.play(sequence)



# Ignore the following




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
