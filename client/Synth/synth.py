import numpy as np
import os
import Synth.LFO
import Synth.osc
import Synth.wavetables
try:
    import alsaaudio
except:
    print('Alsa Audio not found.')
import math
import time
import Synth.envelope
import Synth.filt
import Synth.voice
import wave


class synth:
    '''
        This class is the main combined synthesizer.

        Contains:
            -Two oscilators
            -Two envolopes, one envelope for each oscillator
            -Two filters in series. Both streams get combined then
                passed through the filters
            -Three LFO's for modulation of parameters

        It is recommended that you control everything through the synth class:
            Controls possible with the synth class:

                time is in seconds
                Hz is a frequncy
                bool is a bool
                phase is a float or int corresponding to the phase
                amplitude is a float between 0 and 1
                amplitude(-1) is a float -1 to 1
                semitones is an int corresponding to a semitone
                frame is an int corresponding to a frame of 2048 samples
                cutoff is in Hz

                Synth:
                    volume (amplitude):
                        synth_class_object.volume

                Oscillators (names: oscil and oscil2):

                    Detune (semitones):
                        synth_class_object.<oscilator>.detune

                    Wavetable Position (frame):
                        synth_class_object.<oscilator>.wavetablepos

                    Volume (amplitude):
                        synth_class_object.<oscilator>.volume

                    Phase offset (phase):
                        synth_class_object.<oscilator>.pOffest

                    Disable (bool):
                        synth_class_object.<oscilator>.enable

                    Change wav used for wavetables:
                        synth_class_object.<oscilator>.\
                            set_wavetable(wav='path to file')


                Envelopes (names: env1 and env2):

                    Attack (time):
                        synth_class_object.<envelope>.set_attack(time)

                    Decay (time):
                        synth_class_object.<envelope>.set_decay(time)

                    Sustain (time, amplitude):
                        synth_class_object.<envelope>.\
                            set_sustain(time, amplitude)

                    Release (time):
                        synth_class_object.<envelope>.set_release(time)


                Filters (names: fil1 and fil2):

                    To set as a highpass filter or change the cutoff
                    of a existing highpass:
                        synth_class_object.<filter>.set_cutoff_highpass(cutoff)

                    To set as a lowpass filter or change the cutoff
                    of a existing lowpass:
                        synth_class_object.<filter>.set_cutoff_lowpass(cutoff)

                    Enable (bool):
                        synth_class_object.<filter>.enable

                Low Frequency Oscillators:

                    To set speed (Hz):
                        synth_class_object.<lfo>.set_speed(speed)

                    To set amount (amplitude(-1)):
                        synth_class_object.<lfo>.amount

                    To set offset (amplitude(-1)):
                        synth_class_object.<lfo>.offset

                    To set waveform (str):
                        synth_class_object.<lfo>.waveform

                    Enable (bool):
                        synth_class_object.<lfo>.enable

        Audio playback takes a sequence from the sequencer. It then generates
        the audio for the entire sequence and plays it back through the
        speaker.

            Args:
                volume=0.75 (float) scaling factor for final audio
                    stream amplitude

            Returns:
                None
    '''

    def __init__(self, volume=0.75):
        self.samplerate = 44100
        self.ard_ex = False
        self.volume = volume
        self.feed = list()
        self.record = False
        self.playback = False
        self.playb_dis = False

        # Open audio channel
        try:
            self.aud = alsaaudio.PCM()
            self.aud.setchannels(1)
            self.aud.setrate(self.samplerate)
            self.aud.setformat(alsaaudio.PCM_FORMAT_S16_LE)
            self.mixer = alsaaudio.Mixer()
            self.mixer.setmute(0,0)

        except:
            print('Could not open audio channel.')
            print('Defaulting to record.')
            self.record = True
            self.playb_dis = True

        # Load oscs
        self.oscil = Synth.osc.wtOsc(
            wav='./Synth/wavetables/basic.wav',
            volume=0.75,
            pOffset=1024,
            detune=0,
            wavetablepos=0,
            samplerate=self.samplerate
        )
        self.oscil2 = Synth.osc.wtOsc(
            wav='./Synth/wavetables/basic.wav',
            volume=0.75,
            detune=0,
            wavetablepos=0,
            samplerate=self.samplerate
        )

        # Load Envelopes
        self.env1 = Synth.envelope.envelope(self.samplerate,0.1,2,1,0.5,2)
        self.env2 = Synth.envelope.envelope(self.samplerate,0.1,2,1,0.5,2)

        # Load voices
        self.voices = []
        for i in range(0,8):
            x = Synth.voice.voice(
                self.oscil,
                self.oscil2,
                self.env1,
                self.env2
            )
            self.voices.append(x)

        # Load Filters
        self.fil1 = Synth.filt.filter()
        self.fil2 = Synth.filt.filter()
        self.mix_past = [0,0]
        self.fil1_past = [0,0]

        # Load LFOs
        self.lfo1 = Synth.LFO.lfo(
            self,device=None,
            control=None,
            speed=1,
            amount=0
        )
        self.lfo2 = Synth.LFO.lfo(
            self,device=None,
            control=None,
            speed=1,
            amount=0
        )
        self.lfo3 = Synth.LFO.lfo(
            self,device=None,
            control=None,
            speed=1,
            amount=0
        )


    def gen_freq(self, note, osc):
        '''
            This function takes the note and detune from an wtosc object and
            gives the frequency

                Args:
                    note: (list) containing two elements the string for the
                        note, and the octave.
                                Ex. ['A', 4] = A from the fourth octave
                                Ex. ['FS', 5] = F sharp from the fifth octave

                    osc: (wtosc) Uses to grab the proper detune.

                Returns:
                    (float) corresponding to the frequency
        '''

        tunefreq = 440
        a = 1.059463094359 # 2^(1/12)
        notes = {
            "C":-9,
            "B":2,
            "D":-7,
            "E":-5,
            "F":-4,
            "G":-2,
            "A":0,
            "CS":-8,
            "DS":-6,
            "FS":-3,
            "GS":-1,
            "AS":1
        }


        def _getfreq_(semitonediff):
            freq = tunefreq * (pow(a, semitonediff))
            return freq

        def _getsemitonediff_f0_(note, octave):
            semitonediff = (octave-5)*12
            semitonediff = semitonediff + notes[note]
            return semitonediff


        semitonedif = _getsemitonediff_f0_(note[0], note[1]) + osc.detune
        freq = _getfreq_(semitonedif)
        return freq



    def play(self, sequence):
        '''
            This function takes a squence and generates and plays the audio
            for that sequence.

                Args:
                    sequence (list): containing a note ( ['note',octave] ) and
                                     the time (float corresponding to seconds)
                                     it's played
                                        Ex. [['A',4],4] = Play A 4 for
                                            4 seconds

                Returns:
                    None
        '''
        totaltime = 0
        note_count = 1
        total_notes = len(sequence)
        totalsamples = 0
        samples = []
        for i in self.voices:
            i.in_use = False

        for i in sequence:
            note = i[0]
            time = i[1]
            notesamp = []


            for j in self.voices:
                if j.in_use == False:
                    j.load_note(note, time)
                    numsamples = time * self.samplerate
                    totalsamples += numsamples
                    break

            self.lfo1.get_retrig()
            self.lfo2.get_retrig()
            self.lfo3.get_retrig()

            count = 0
            if not note == None:
                print('Rendering {} {}. ({}/{})'.format(
                    note[0],note[1], note_count, total_notes
                ))
            else:
                print('Rendering rest. ({}/{})'.format(note_count,total_notes))

            note_count += 1

            while count < numsamples:
                # This is the order the synth will run

                # Run LFO's
                self.lfo1.update_control(self.lfo1.device, self.lfo1.control)
                self.lfo2.update_control(self.lfo2.device, self.lfo2.control)
                self.lfo3.update_control(self.lfo3.device, self.lfo3.control)

                tot = 0
                sig_count = 0

                for j in self.voices:
                    if j.in_use == True:
                        out = j.genOutput()
                        if not (out == None or out[0] == 0):
                            tot += out[0]
                            sig_count += out[1]

                tot = tot//2
                # Limits the feed, if tot > 100% volume clip it to 100%
                if tot > 32767:
                    tot = 32767
                elif tot < -32768:
                    tot = -32768

                output = tot
                del self.mix_past[0]
                self.mix_past.append(output)

                # Feeds into the filter's

                self.fil1_past.append(self.fil1.generate_output(self.mix_past))
                del self.fil1_past[0]
                output = self.fil2.generate_output(self.fil1_past)

                # Limits the feed, if tot > 100% volume clip it to 100%
                if output > 32767:
                    output = 32767
                elif output < -32768:
                    output = -32768

                notesamp.append(output*self.volume)
                count += 1

            samples.append(notesamp)
        totalsamples = math.floor(totalsamples)




        if self.record == True:
            print('Recording to output.wav...')
            if os.path.exists('output.wav'):
                os.remove('output.wav')

            with wave.open('output.wav', mode='wb') as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(44100)
                wav.setnframes(len(samples))

                for i in samples:
                    wav.writeframes(np.int16(i))


        try:

            self.aud.setperiodsize((totalsamples*2))

            if self.playback == True:
                print("Playing...")
                for i in samples:
                    self.aud.write(np.int16(i))

        except:
            pass
