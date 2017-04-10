import Synth.osc
import Synth.envelope
import math

class voice:

    def __init__(self, osc1, osc2, env1, env2, notetime=0, freq1=0, phase1=0, freq2=0, phase2=0, samplerate=44100):
        self.samplerate = samplerate
        self.osc1 = osc1
        self.osc2 = osc2
        self.env1 = env1
        self.env2 = env2
        self.curr_sample = 0
        self.notesamp = samplerate*notetime
        self.release1 = self.env1.releasesamples
        self.release2 = self.env2.releasesamples
        self.freq1 = freq1
        self.freq2 = freq2
        self.phase1 = phase1
        self.phase2 = phase2
        self.in_use = False


    def load_note(self, note, time):
        if not note == None:
            self.note = note
            self.freq1 = self.osc1.gen_freq(self.note)
            self.freq2 = self.osc2.gen_freq(self.note)
            self.phase1 = self.osc1.pOffset
            self.phase2 = self.osc2.pOffset
            self.notesamp = self.samplerate * time
            self.curr_sample = 0
            self.in_use = True

        else:
            pass

    def genOutput(self):
        if self.curr_sample > self.notesamp:
            self.in_use = False
            return None
        else:
            self.osc1.freq = self.osc1.gen_freq(self.note)
            self.osc2.freq = self.osc2.gen_freq(self.note)
            self.osc1.phase = self.phase1
            self.osc2.phase = self.phase2
            sig1 = self.osc1.genOutput()
            sig2 = self.osc2.genOutput()
            self.phase1 = self.osc1.phase
            self.phase2 = self.osc2.phase

            sus_samples1 = self.notesamp - self.env1.attacksamples - self.env1.decaysamples - self.env1.releasesamples
            sus_samples2 = self.notesamp - self.env2.attacksamples - self.env2.decaysamples - self.env2.releasesamples

            if sus_samples1 < 0:
                sus_samples1 = 0
            if sus_samples2 < 0:
                sus_samples2 = 0

            self.env1.sustainsamples = sus_samples1
            self.env2.sustainsamples = sus_samples2

            # Feed into envelope
            sig1 = self.env1.gen_env(self.curr_sample, sig1)
            sig2 = self.env2.gen_env(self.curr_sample, sig2)

            tot = 0
            sig_count = 0
            if not sig1 == None:
                tot += sig1
                sig_count += 1

            if not sig2 == None:
                tot += sig2
                sig_count += 1

            self.curr_sample += 1

            return [tot, sig_count]
