import math

class wtOsc:
    '''
        This class is a wavetable oscillator that can be controlled by phasor, frequency,
        wavetable position, detune, and volume. Phases offset is not implemented yet

        Using the genOutput function you can generate one sample at the current phase,
        looping it will produce a sound data stream.

            Args:
                phasor=0    float, allows the ability to set the phasor value

                pOffest=0.5     int, notimplemented

                wave_tables=None    wavetable

                samplerate=44100    int, frequncy samples are generated

                detune=0    int -24 to 24, the number of semitones to detune from original note

                wavetablepos=0     int 0 to n, where n is the number of frames in the wave table.
                                        Sets which frame to use

                volume=1    float 0 to 1, The amplitude scaling factor

            Returns:
                none
    '''

    def __init__(self, phasor=0, pOffset=0.5, wave_tables=None, samplerate=44100, detune=0, wavetablepos=0, volume=1):
        self.wavetsize = 2048
        self.wave_tables = wave_tables
        self.samplerate = samplerate
        self.phasor = phasor
        self.pInc = 0
        self.enable = True

        # min max and step used by the LFO
        self.pOffset = pOffset
        self.pOffset_max = self.wavetsize
        self.pOffest_min = 0
        self.pOffest_step = 1

        self.detune = detune
        self.detune_max = 24
        self.detune_min = -24
        self.detune_step = 1

        self.wavetablepos = wavetablepos * 2048
        self.wavetablepos_min = 0
        self.wavetablepos_max = 1 #for now wavetables need to be finished
        self.wavetablepos_step = 1

        self.volume = volume
        self.volume_min = 0
        self.volume_max = 1
        self.volume_step = 0.01






    def genOutput(self, freq=None):
        '''
            This function generates one audio sample

                Args:
                    freq=None    float, this is the output frequency of the stream

                Returns:
                    float,  corresponding to a audio sample
        '''
        # calculates the phase increment based on the formula:
        # pinc = N * f / fs
        # where N is the number of steps in the wave table
        #       f is the frequency we want to generate
        #       fs is the sample frequency or sample rate
        if self.enable == False:
            return 0
        if not freq:
            return 0

        self.pInc = self.wavetsize * (freq / self.samplerate)
        self.phasor = self.phasor + self.pInc

        # Checks that adding the offset does not place the phase out of the window
        if self.phasor >= (self.wavetablepos + 2048):
            self.phasor = self.phasor - self.wavetsize + 1

        output = (self.wave_tables[math.floor(self.phasor)])

        if output > 32768:
            output = (65536 - output)*self.volume
        else:
            output = output*self.volume

        return output
