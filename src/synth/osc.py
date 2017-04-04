import math

class wtOsc:
    # I recommend not changing these values
    tunefreq = 440
    a = 1.059463094359 # 2^(1/12)
    notes = {"C":-9,"B":2,"D":-7,"E":-5,"F":-4,"G":-2,"A":0,"CS":-8,"DS":-6,"FS":-3,"GS":-1,"AS":1}                    # Semi tone displacement from A

    #TODO: Write documentaion this is basically done


    def __init__(self, phasor=0, pInc=0, pOffset=0.5, wave_tables=None, samplerate=22050, detune=0, wavetablepos=0):
        self.phasor = phasor
        self.pInc = pInc
        self.pOffset = pOffset
        self.wave_tables = wave_tables
        self.wavetsize = len(self.wave_tables)
        self.samplerate = samplerate
        self.detune = detune
        self.wavetablepos = wavetablepos


    def genOutput(self, note=None, freq=None):
        # calculates the phase increment based on the formula:
        # pinc = N * f / fs
        # where N is the number of steps in the wave table
        #       f is the frequency we want to generate
        #       fs is the sample frequency or sample rate


        if not freq:
            if not note:
                return 0

            semitonediff = self._getsemitonediff_f0_(note[0], note[1]) + self.detune
            freq = self._getfreq_(semitonediff)

        self.pInc = self.wavetsize * (freq / self.samplerate)
        self.phasor = self.phasor + self.pInc

        # Checks that adding the offset does not place the phase out of the window
        if self.phasor >= self.wavetsize:
            self.phasor = self.phasor - self.wavetsize + 1

        output = self.wave_tables[math.floor(self.phasor)]

        return output




    def _getfreq_(self, semitonediff):
        freq = self.tunefreq * (pow(self.a, semitonediff))
        return freq

    def _getsemitonediff_f0_(self, note, octave):
        semitonediff = (octave-4)*12
        semitonediff = semitonediff + self.notes[note]
        return semitonediff
