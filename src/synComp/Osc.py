import math

class wto:

    def __init__(self, phasor=0, pInc=0, pOffset=0.5, wave_tables=None, samplerate=22050):
        self.phasor = phasor
        self.pInc = pInc
        self.pOffset = pOffset
        self.wave_tables = wave_tables


    def genOutput(self, freq):
        print(self.phasor)
        pInc = len(self.wave_tables) * freq / self.samplerate

        if self.phasor + self.pInc >= len(self.wave_tables):
            self.phasor = phasor + pInc - len(self.wave_tables) - 1

        else:
            self.phasor = self.phasor + self.pInc


        output = self.wave_tables[floor(phasor)]

        return output
