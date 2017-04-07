import math

class envelope:
    '''
        This class creates an envelope that outputs a scaling value based on
        the amount of time that has 'passed'

            Args:
                samplerate: int, corresponding to Hz

                attack: float, corresponding to seconds

                decay: float, corresponding to seconds

                sustain: float, corresponding to seconds

                release: float, corresponding to seconds, zero by default, not implemented

            Returns:
                nothing
    '''

    def __init__(self, samplerate, attack, decay, sustain, sustain_amp, release):
        self.attacksamples = attack * samplerate
        self.decaysamples = decay * samplerate
        self.sustainsamples = sustain * samplerate
        self.sustain_amp = sustain_amp
        self.releasesamples = release * samplerate
        self.samplerate = samplerate

    def set_attack(self, time):
        self.attacksamples = time * self.samplerate

    def set_decay(self, time):
        self.decaysamples = time * self.samplerate

    def set_sustain(self, time, amp):
        self.sustain_amp = amp
        self.sustainsamples = time * self.samplerate

    def set_release(self, time):
        self.releasesamples = time * self.samplerate

    def gen_env(self, curr_sample, inp):
        '''
        This function outputs the scaling factor based on the current sample

            Args:
                curr_sample: int, corresponding to the current sample number being processed

                inp:    float, corresponding to an input audio stream

            Returns:
                float, corresponding to the scaled suadio stream
        '''

        if curr_sample < self.attacksamples:
            return (curr_sample/self.attacksamples) * inp

        elif (curr_sample - self.attacksamples) < self.decaysamples:
            return (((self.sustain_amp - 1)/self.decaysamples)*(curr_sample - self.attacksamples) + 1) * inp

        elif (curr_sample - self.decaysamples - self.attacksamples) < self.sustainsamples:
            return self.sustain_amp * inp

        elif (curr_sample - self.decaysamples - self.attacksamples - self.sustainsamples) <= self.releasesamples:
            sample = (curr_sample - self.decaysamples - self.attacksamples - self.sustainsamples)
            return ((-self.sustain_amp/self.releasesamples)*sample + self.sustain_amp) * inp

        else:
            return 0
