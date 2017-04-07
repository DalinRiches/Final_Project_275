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
        self.phasor = phasor
        self.pInc = 0
        self.pOffset = pOffset
        self.wave_tables = wave_tables
        self.wavetsize = 2048
        self.samplerate = samplerate
        self.detune = detune
        self.wavetablepos = wavetablepos * 2048
        self.volume = volume


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
