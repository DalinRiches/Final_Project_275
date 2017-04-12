import math
import Synth.wavetables

class wtOsc:
    '''
        This class is a wavetable oscillator that can be controlled by phasor,
        frequency, wavetable position, detune, and volume. Phases offset is
        not implemented yet

        Using the genOutput function you can generate one sample at the current
        phase, looping it will produce a sound data stream.

            Args:
                phasor=0: (float) allows the ability to set the phasor value

                pOffest=0.5: (int) 0 to 2048, Allows phase shifting of an osc

                samplerate=44100: (int) frequency samples are generated

                detune=0: (int) -24 to 24, the number of semitones to detune
                    from original note

                wavetablepos=0: (int) 0 to n, where n is the number of frames
                                in the wave table. Sets which frame to use

                volume=1: (float) 0 to 1, The amplitude scaling factor

            Returns:
                None
    '''

    def __init__(self, pOffset=0, wav=None, samplerate=44100, detune=0,
                 wavetablepos=0, volume=1):
        self.wavetable = Synth.wavetables.wavetable()
        self.wavetsize = 2048
        self.set_wavetable(wav)
        self.samplerate = samplerate
        self.note = None
        self.freq = 0
        self.pOffset = pOffset
        self.phasor = self.pOffset
        self.pInc = 0
        self.enable = True

        # min max and step used by the LFO

        self.pOffset_max = self.wavetsize
        self.pOffest_min = 0
        self.pOffest_step = 1

        self.detune = detune
        self.detune_max = 24
        self.detune_min = -24
        self.detune_step = 1

        self.wavetablepos = wavetablepos * 2048
        self.wavetablepos_min = 0
        self.wavetablepos_max = self.wave_tables_num - 1
        self.wavetablepos_step = 1

        self.volume = volume
        self.volume_min = 0
        self.volume_max = 1



    def set_wavetable(self, wav=None):
        if wav == None:
            return

        self.wave_tables = self.wavetable.parse_wavtab(wav=wav)
        self.wave_tables_num = len(self.wave_tables)/self.wavetsize


    def gen_freq(self, note=None):
        '''
            This function takes the note and detune from an wtosc object and
            gives the frequency

                Args:
                    note: (list) containing two elements the string for the
                          note, and the octave.
                                Ex. ['A', 4] = A from the fourth octave
                                Ex. ['FS', 5] = F sharp from the fifth octave

                    osc: (wtosc) Uses to grab the proper detune.

                Returns:
                    (float) corresponding to the frequency
        '''
        if not note == None:
            self.note = note

        tunefreq = 440
        a = 1.059463094359 # 2^(1/12)
        notes = {
            "C":-9,
            "B":2,
            "D":-7,
            "E":-5,
            "F":-4,
            "G":-2,
            "A":0,
            "CS":-8,
            "DS":-6,
            "FS":-3,
            "GS":-1,
            "AS":1
        }


        def _getfreq_(semitonediff):
            freq = tunefreq * (pow(a, semitonediff))
            return freq

        def _getsemitonediff_f0_(note, octave):
            semitonediff = (octave-5)*12
            semitonediff = semitonediff + notes[note]
            return semitonediff


        semitonedif = _getsemitonediff_f0_(
            self.note[0], self.note[1]
        ) + self.detune
        freq = _getfreq_(semitonedif)
        return freq


    def genOutput(self):
        '''
            This function generates one audio sample

                Args:
                    freq=None (float) this is the output frequency of
                        the stream

                Returns:
                    (float) corresponding to a audio sample
        '''
        # calculates the phase increment based on the formula:
        # pinc = N * f / fs
        # where N is the number of steps in the wave table
        #       f is the frequency we want to generate
        #       fs is the sample frequency or sample rate
        if self.enable == False:
            return 0

        self.pInc = self.wavetsize * (self.freq / self.samplerate)
        self.phasor = self.phasor + self.pInc

        # Checks that adding the offset does not place the phase
        # out of the window
        if self.phasor >= (self.wavetablepos + 2048):
            self.phasor = self.phasor - self.wavetsize + 1

        output = (self.wave_tables[math.floor(self.phasor)])

        if output > 32768:
            output = (65536 - output)*self.volume
        else:
            output = output*self.volume

        return output
