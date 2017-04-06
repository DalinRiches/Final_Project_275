
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

    def __init__(self, samplerate, attack, decay, sustain, sustain_amp, release=0):
        self.attacksamples = attack * samplerate
        self.decaysamples = decay * samplerate
        self.sustainsamples = sustain * samplerate
        self.sustain_amp = sustain_amp
        self.releasesamples = 0
        self.samplerate = samplerate

    def gen_env(self, curr_sample):
        '''
        This function outputs the scaling factor based on the current sample

            Args:
                curr_sample: int, corresponding to the current sample number being processed

            Returns:
                float from 0 to 1
        '''
        if curr_sample < self.attacksamples:
            return curr_sample/self.attacksamples

        elif (curr_sample - self.decaysamples) < self.decaysamples:
            return 1

        elif (curr_sample - self.decaysamples - self.attacksamples) < self.sustainsamples:
            num = (((self.sustain_amp - 1)/self.sustainsamples)*(curr_sample - self.decaysamples - self.attacksamples) + 1)
            
            return num

        else:
            return 0
