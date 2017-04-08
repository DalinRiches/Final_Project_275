import math

class filter:

    def __init__(self, samplerate=44100):
        self.samplerate = samplerate
        self.filtertype = 'Low Pass'
        self.past_output = 0
        self.enable = True

        # min max and step used by LFO
        self.set_cutoff_highpass(100)
        self.set_cutoff_highpass_max = 20000
        self.set_cutoff_highpass_min = 1 #can't be zero
        self.set_cutoff_highpass_step = 1

        self.set_cutoff_lowpass(10000)
        self.set_cutoff_lowpass_max = 20000
        self.set_cutoff_lowpass_min = 1 #can't be zero
        self.set_cutoff_lowpass_step = 1



    def set_cutoff_highpass(self, cutoff):
        self.cutoff_hp = cutoff
        self.alpha_hp = 1 / (2 * math.pi * (1/self.samplerate) * self.cutoff_hp)
        self.filtertype = 'High Pass'

    def set_cutoff_lowpass(self, cutoff):
        self.cutoff_lp = cutoff
        self.alpha_lp = ((2* math.pi * (1/self.samplerate) * self.cutoff_lp)/(((2* math.pi * (1/self.samplerate))+1)))
        self.filtertype = 'Low Pass'



    def generate_output(self, inp):
        if self.enable == False:
            return inp[1]

        if self.filtertype == 'High Pass':
            output = (self.alpha_hp * (self.past_output + inp[0] - inp[1]))
            self.past_output = output
            return output

        elif self.filtertype == 'Low Pass':
            output = (self.past_output + (self.alpha_lp *(inp[0] - self.past_output)))
            self.past_output = output
            return output
