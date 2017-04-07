import numpy as np
import serial
import Synth.osc
import Synth.wavetables
import alsaaudio
import math
import time
import Synth.envelope
import Synth.filt


class synth:
    '''
        This class is the main combined synthesizor this will generate audio
        from the speakers, in the future downloading to arduino for playback
        will be supported.

        Contains:
            -Two oscilator's
            -An envelope for each oscillator
            -Two filter's in series. Both streams get combined then passed through the first
            -A single delay the filtered stream is passed through    (Might Implemente)
            -Three LFO's for modulation of parameter's   (Not implemented)

        It is recommended that you control everything through the synth class:
            Controls possible with the synth class:


                Oscillator's (names: oscil and oscil2):

                    Detune (semitones):
                        synth_class_object.<oscilator>.detune

                    Wavetable Position (frame):
                        synth_class_object.<oscilator>.wavetablepos

                    Volume (scaling factor from 0 to 1):
                        synth_class_object.<oscilator>.volume

                    Phase offset (phase):
                        synth_class_object.<oscilator>.pOffest

                    Disable (bool):
                        synth_class_object.<oscilator>.enable


                Envelope's (names: env1 and env2):

                    Attack (time):
                        synth_class_object.<envelope>.set_attack(time)

                    Decay (time):
                        synth_class_object.<envelope>.set_decay(time)

                    Sustain (time, amplitude):
                        synth_class_object.<envelope>.set_sustain(time, amplitude)

                    Release (time):
                        synth_class_object.<envelope>.set_release(time)


                Filter's (names: fil1 and fil2):

                    To set as a highpass filter or change the cutoff of a existing highpass:
                        synth_class_object.<filter>.set_cutoff_highpass(cutoff)

                    To set as a lowpass filter or change the cutoff of a existing lowpass:
                        synth_class_object.<filter>.set_cutoff_lowpass(cutoff)


                Changing wavetables is not supported yet.


        Audio playback takes a sequence from the sequencer, which will be made in the GUI.
        It then generates the audio for the entire sequence and plays it back through the speaker.
        If set to upload to arduino it does not output to speakers and converts the bitstream from
        PCM_FORMAT_S16_LE to uint8_t which the arduino downloads and plays on reset
            -For arduino download the arduino only has 8KB of SRAM so if we cut the samplerate
                to 22050 Hz we can upload ~0.37 seconds of sound data.

            Args:
                volume=0.75    float, scaling factor for final audio stream amplitude

            Returns:
                None
    '''

    def __init__(self, volume=0.75):
        self.samplerate = 44100
        self.ard_ex = False
        self.volume = volume
        self.feed = list()

        # Open audio channel
        self.aud = alsaaudio.PCM(mode=alsaaudio.PCM_NONBLOCK)
        self.aud.setchannels(1)
        self.aud.setrate(self.samplerate)
        self.aud.setformat(alsaaudio.PCM_FORMAT_S16_LE)

        # Load default wavetables
        self.wave_tables = Synth.wavetables.wavetable(wav='./Synth/Basic Shapes.wav')
        self.wave_tables2 = Synth.wavetables.wavetable(wav='./Synth/Basic Shapes.wav')

        # Load osc's
        self.oscil = Synth.osc.wtOsc(wave_tables=self.wave_tables.table, volume=0.75, detune=12, wavetablepos=0, samplerate=self.samplerate)
        self.oscil2 = Synth.osc.wtOsc(wave_tables=self.wave_tables.table, volume=0.75, detune=0, wavetablepos=0, samplerate=self.samplerate)

        # Load Envolopes
        self.env1 = Synth.envelope.envelope(self.samplerate,0.1,0.5,0.5,0.7,0.5)
        self.env2 = Synth.envelope.envelope(self.samplerate,0.1,0.5,0.5,0.7,0.5)

        # Load Filter's
        self.fil1 = Synth.filt.filter()
        self.fil2 = Synth.filt.filter()
        self.mix_past = [0,0]
        self.fil1_past = [0,0]

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
            notesamp = []
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


                # Feed into envelope
                sig1 = self.env1.gen_env(count, sig1)
                sig2 = self.env2.gen_env(count, sig2)


                tot = 0
                if not sig1 == None:
                    tot += sig1

                if not sig2 == None:
                    tot += sig2

                #mixes the feed
                tot = (tot//math.sqrt(2))*self.volume

                # Limits the feed, if tot > 100% volume clip it to 100%
                if tot > 32768:
                    tot = 32768
                elif tot < -32768:
                    tot = -32768

                output = tot
                del self.mix_past[0]
                self.mix_past.append(output)

                # Feeds into the filter's

                self.fil1_past.append(self.fil1.generate_output(self.mix_past))
                del self.fil1_past[0]
                output = self.fil2.generate_output(self.fil1_past)

                notesamp.append(output)
                count += 1

            samples.append(notesamp)

        self.aud.setperiodsize((totalsamples*2) -1)

        if ard_rec == False:
            for i in samples:
                self.aud.write(np.int16(i))
        else:
            ard_bytes = []
            for i in range(0,8100):

                if samples[0][i] > 0:

                    ard_bytes.append(math.floor((samples[0][i]/32768) * 255))
                elif samples[0][i] < 0:

                    ard_bytes.append(math.floor(255 - ((samples[0][i]/32768) * 255)))

                else:
                    ard_bytes.append(0)



            try:
                print(ard_bytes)
                with serial.Serial(port='/dev/ttyACM13', baudrate=9600) as ser:

                    while(True):
                        if ser.in_waiting > 0:
                            junk = ser.read(1)

                        if ser.in_waiting == 0:
                            break

                    time.sleep(5)
                    count = 0
                    ser.write(b'RRR')
                    for i in range(0, 8100):
                        count += 1
                        ser.write(b'T')
                        ser.write(bytes([ard_bytes[i],]))

                        print(count)
                        while(True):
                            reply = ser.read(1)
                            if reply == b'R':
                                break

            except serial.SerialException:
                print("Could not open port")





if __name__ == "__main__":

    syn = synth();
    sequence = [[['A',3],4],[['G',3],4],[['F',3],4],[['A',3],2],[['G',3],2],[['F',3],0.5],[['A',3],0.5],
                    [['G',3],1],[['F',3],1]]

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
