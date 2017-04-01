import math

class wtOsc:


    def __init__(self, phasor=0, pInc=0, pOffset=0.5, wave_tables=None, samplerate=22050):
        self.phasor = phasor
        self.pInc = pInc
        self.pOffset = pOffset
        self.wave_tables = wave_tables
        self.samplerate = samplerate


    def genOutput(self, freq):
        # calculates the phase increment based on the formula:
        # pinc = N * f * fs
        # where N is the number of steps in the wave table
        #       f is the frequency we want to generate
        #       fs is the sample frequency or sample rate
        self.pInc = len(self.wave_tables) * freq / self.samplerate

        self.phasor = self.phasor + self.pInc

        # Checks that adding the offset does not place the phase out of the window
        if self.phasor + self.pOffset > len(self.wave_tables) - 1:
            self.phasor = self.phasor + self.pInc - len(self.wave_tables) + 1 + self.pOffset

        output = self.wave_tables[math.floor(self.phasor + self.pOffset)]

        return output

        #not implemented yet
    def genOutput_no(self, freq):
        pass
