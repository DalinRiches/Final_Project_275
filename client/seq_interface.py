# For graphics
import tkinter
from tkinter.constants import *

# Custom widget-like definitions
import synthwidget
import newseqwidget
import dialwidget

# Synthesizer
import Synth


class PlaybackController:
    ''' Represents the overall structure of the playback sequence.
    seqsource contains a function that generates a sequence of notes. '''

    def __init__(self, synth):
        self.synth = synth
        self.seqsource = None
        self._play_speed = 0.5


    def get_sequence(self):
        print("Getting sequence...")
        seq = self.seqsource()
        print(seq)
        return seq


    def set_play_speed(self, value):
        ''' Sets the play speed. '''
        self._play_speed = value


    def get_play_speed(self):
        ''' Gets the play speed. '''
        return self._play_speed


    def play(self):
        seq = self.get_sequence()
        print("Rendering...")
        self.synth.play(seq, slide=True)
        print("Done.")
        print("Playing...")



def gen_controlbar(tk, ctrl):
    ''' Creates the main playback control bar, with a Play button
    and a speed (reciprocal tempo) dial. '''

    bar = tkinter.Frame(
        tk,
        bd=2,
        relief=RAISED
    )

    bar_dial = dialwidget.Dial(
        bar,
        label="Speed",
        dmin=0.2, dmax=2.0,
        dinitial=0.5,
        callback=ctrl.set_play_speed
    )

    bar_play = tkinter.Button(
        bar,
        bg="green",
        text="Play",
        font="Fixed 9",
        command=ctrl.play
    )

    bar_dial.pack(side=LEFT)
    bar_play.pack(side=LEFT)

    return bar


def setup(synth):
    ''' Sets up the interface and returns a reference to
    the base Tk widget. '''

    ctrl = PlaybackController(synth)

    tk = tkinter.Tk()

    seq = newseqwidget.Sequencer(
        parent=tk,
        length=50,
        height=24,
        firstnoteidx=3*12-1, # (index of C3)
        temposource=ctrl.get_play_speed
    )

    ctrl.seqsource = seq.sequence

    oscframe = tkinter.Frame()

    osc1ct = synthwidget.OscPanel(
        parent=oscframe,
        target=synth.oscil
    )
    osc2ct = synthwidget.OscPanel(
        parent=oscframe,
        target=synth.oscil2
    )
    filt1ct = synthwidget.FiltPanel(
        parent=oscframe,
        target=synth.fil1
    )

    osc1ct.pack(side=LEFT, fill=X)
    osc2ct.pack(side=LEFT, fill=X)
    filt1ct.pack(side=LEFT, fill=X)
    oscframe.pack(side=TOP)

    envframe = tkinter.Frame()

    env1ct = synthwidget.EnvPanel(
        parent=envframe,
        target=synth.env1
    )
    env2ct = synthwidget.EnvPanel(
        parent=envframe,
        target=synth.env2
    )
    filt2ct = synthwidget.FiltPanel(
        parent=envframe,
        target=synth.fil2
    )

    env1ct.pack(side=LEFT, fill=X)
    env2ct.pack(side=LEFT, fill=X)
    filt2ct.pack(side=LEFT, fill=X)
    envframe.pack(side=TOP)

    lfoframe = tkinter.Frame()

    lfo1ct = synthwidget.LFOPanel(
        parent=lfoframe,
        target=synth.lfo1
    )
    lfo2ct = synthwidget.LFOPanel(
        parent=lfoframe,
        target=synth.lfo2
    )
    lfo3ct = synthwidget.LFOPanel(
        parent=lfoframe,
        target=synth.lfo3
    )

    lfo1ct.bind_to_synth(synth)
    lfo2ct.bind_to_synth(synth)
    lfo3ct.bind_to_synth(synth)

    lfo1ct.pack(side=LEFT, fill=X)
    lfo2ct.pack(side=LEFT, fill=X)
    lfo3ct.pack(side=LEFT, fill=X)
    lfoframe.pack(side=TOP)

    ctrlbar = gen_controlbar(tk, ctrl)
    ctrlbar.pack(side=TOP)

    # NOTE seq must be packed last so that if the window runs
    # out of room it loses seq rows, instead of more important
    # things like oscillator dials.
    seq.pack(side=BOTTOM)

    return tk


if __name__ == '__main__':
    synthesizer = Synth.synth()

    tk = setup(synthesizer)

    tk.mainloop()
