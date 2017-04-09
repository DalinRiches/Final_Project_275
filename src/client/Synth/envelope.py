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
        self.releases = []

        # Used by LFO
        self.attack_min = 0
        self.attack_max = 5

        self.decay_min = 0
        self.decay_max = 5

        self.sustain_min = 0
        self.sustain_max = 5

        self.sustain_amp_min = 0
        self.sustain_amp_max = 1
        self.suatian_amp_step = 0.01

        self.release_min = 0
        self.release_max = 5




    def set_attack(self, time):
        self.attacksamples = time * self.samplerate

    def set_decay(self, time):
        self.decaysamples = time * self.samplerate

    def set_sustain(self, time, amp):
        self.sustain_amp = amp
        self.sustainsamples = time * self.samplerate

    def set_release(self, time):
        self.releasesamples = time * self.samplerate

    def get_releases(self, osc):
        old_phasor = osc.phasor
        old_freq = osc.freq
        len_releases = len(self.releases)
        if len_releases <= 0:
            return 0
        tot = 0
        for i in self.releases:
            osc.freq = i[0]
            osc.phase = i[1]
            curr = i[2]
            totsamp = i[3]
            sus_amp = i[4]

            val = osc.genOutput()
            tot += ((-sus_amp/totsamp)*curr + sus_amp)*val
            i[2] += 1


        osc.phasor = old_phasor
        osc.freq = old_freq
        output = [tot,len_releases]
        return output

    def gen_env_graph(self, curr_sample, inp):
        '''
        This function outputs the scaling factor based on the current sample
            Args:
                curr_sample: int, corresponding to the current sample number being processed
                inp:    float, corresponding to an input audio stream
            Returns:
                float, corresponding to the scaled suadio stream
        '''

        if curr_sample < self.attacksamples and not self.attacksamples == 0:
            return (curr_sample/self.attacksamples) * inp

        elif ((curr_sample - self.attacksamples) < self.decaysamples) and not self.decaysamples == 0:
            return (((self.sustain_amp - 1)/self.decaysamples)*(curr_sample - self.attacksamples) + 1) * inp

        elif (curr_sample - self.decaysamples - self.attacksamples) < self.sustainsamples:
            return self.sustain_amp * inp

        elif (curr_sample - self.decaysamples - self.attacksamples - self.sustainsamples) <= self.releasesamples and not self.releasesamples == 0:
            sample = (curr_sample - self.decaysamples - self.attacksamples - self.sustainsamples)
            return ((-self.sustain_amp/self.releasesamples)*sample + self.sustain_amp) * inp

        else:
            return 0

    def gen_env(self, curr_sample, totsample, inp, freq, phase):
        '''
        This function outputs the scaling factor based on the current sample

            Args:
                curr_sample: int, corresponding to the current sample number being processed

                inp:    float, corresponding to an input audio stream

            Returns:
                float, corresponding to the scaled suadio stream
        '''

        if curr_sample < self.attacksamples and not self.attacksamples == 0:
            return (curr_sample/self.attacksamples) * inp

        elif ((curr_sample - self.attacksamples) < self.decaysamples) and not self.decaysamples == 0:
            return (((self.sustain_amp - 1)/self.decaysamples)*(curr_sample - self.attacksamples) + 1) * inp

        elif curr_sample < (totsample - 1):
            return self.sustain_amp * inp

        elif curr_sample == (totsample-1):
            if freq == 0:
                return 0

            self.releases.append([freq, phase, 0, self.releasesamples, self.sustain_amp])
