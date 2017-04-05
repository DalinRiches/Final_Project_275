import math

class envolope:

    def __init__(self, samplerate, attack, decay, sustain, release=0):
        self.attacksamples = attack * samplerate
        self.decaysamples = decay * samplerate
        self.sustainsamples = sustain * samplerate
        self.releasesamples = 0
        self.samplerate = samplerate

    def gen_env(self, curr_sample):
        if curr_sample < self.attacksamples:
            return curr_sample/self.attacksamples

        elif (curr_sample - self.decaysamples) < self.decaysamples:
            return 1

        elif (curr_sample - self.decaysamples - self.attacksamples) < self.sustainsamples:
            num = curr_sample - self.decaysamples - self.attacksamples
            return (1 - num/self.sustainsamples)

        else:
            return 0
