# For graphics
import tkinter
from tkinter.constants import *

# Custom widget-like definitions
import synthwidgets
import seqwidget
import dialwidget

# Synthesizer
import Synth


class PlaybackController:
    ''' Represents the overall structure of the playback sequence.
    seqsource contains a function that generates a sequence of notes. '''

    def __init__(self, synth):
        ''' Initializer for PlaybackController. Just sets up data. '''

        # regular data
        self.synth = synth

        # sequence source, will be set later
        self.seqsource = None

        # current speed
        self._play_speed = 0.5


    def get_sequence(self):
        ''' Retrieves and returns a sequence of notes from the
        configured seqsource. seqsource is set externally. '''
        print("Getting sequence...")
        seq = self.seqsource()
        return seq


    def set_play_speed(self, value):
        ''' Sets the play speed. '''
        self._play_speed = value


    def get_play_speed(self):
        ''' Gets the play speed. '''
        return self._play_speed


    def play(self):
        ''' Invokes the synthesizer to play the sequence available
        in seqsource. '''
        seq = self.get_sequence()
        print("Rendering...")
        self.synth.play(seq)
        print("Done.")


    def record(self):
        ''' Like self.play, but invokes synth.record. '''
        seq = self.get_sequence()
        print("Rendering...")
        self.synth.record(seq)
        print("Done recording.")


def gen_controlbar(tk, ctrl):
    ''' Creates the main playback control bar, with a Play button
    and a speed (reciprocal tempo) dial. '''

    bar = tkinter.Frame(
        tk,
        bd=2,
        relief=RAISED,
        bg="black"
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

    bar_rec = tkinter.Button(
        bar,
        bg="gray50",
        text="Record",
        font="Fixed 9",
        command=ctrl.record
    )

    bar_rec.pack(side=BOTTOM, expand=1)
    bar_dial.pack(side=LEFT)
    bar_play.pack(side=LEFT, expand=1, pady=3)

    return bar


def setup(synth):
    ''' Sets up the interface and returns a reference to
    the base Tk widget. '''

    # Main window
    tk = tkinter.Tk()
    tk.title("Synthesizer")
    tk.config(bg='black')

    # Playback controller
    ctrl = PlaybackController(synth)

    # Sequencer
    seq = seqwidget.Sequencer(
        parent=tk,
        length=42,
        height=24,
        firstnoteidx=3*12-1, # (index of C3)
        temposource=ctrl.get_play_speed
    )

    # Bind playback controller to sequencer
    # (NOTE the bindings are circular; neither
    # can entirely initialized before the other,
    # so the cycle is closed here.)
    ctrl.seqsource = seq.sequence

    # First frame row: oscillators and filter 1
    oscframe = tkinter.Frame(bg="black")

    osc1ct = synthwidgets.OscPanel(
        parent=oscframe,
        target=synth.oscil
    )
    osc2ct = synthwidgets.OscPanel(
        parent=oscframe,
        target=synth.oscil2
    )
    filt1ct = synthwidgets.FiltPanel(
        parent=oscframe,
        target=synth.fil1
    )

    osc1ct.pack(side=LEFT, fill=X)
    osc2ct.pack(side=LEFT, fill=X)
    filt1ct.pack(side=LEFT, fill=X)
    oscframe.pack(side=TOP)


    # Second frame row: envelopes and filter 2
    envframe = tkinter.Frame(bg="black")

    env1ct = synthwidgets.EnvPanel(
        parent=envframe,
        target=synth.env1
    )
    env2ct = synthwidgets.EnvPanel(
        parent=envframe,
        target=synth.env2
    )
    filt2ct = synthwidgets.FiltPanel(
        parent=envframe,
        target=synth.fil2
    )

    env1ct.pack(side=LEFT, fill=X)
    env2ct.pack(side=LEFT, fill=X)
    filt2ct.pack(side=LEFT, fill=X)
    envframe.pack(side=TOP)


    # Third frame row: LFOs
    lfoframe = tkinter.Frame(bg="black")

    lfo1ct = synthwidgets.LFOPanel(
        parent=lfoframe,
        target=synth.lfo1
    )
    lfo2ct = synthwidgets.LFOPanel(
        parent=lfoframe,
        target=synth.lfo2
    )
    lfo3ct = synthwidgets.LFOPanel(
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


    # Playback panel
    ctrlbar = gen_controlbar(tk, ctrl)
    ctrlbar.pack(side=RIGHT, fill=X, expand=1, anchor=N)


    # NOTE seq must be packed last so that if the window runs
    # out of room it loses seq rows, instead of more important
    # things like panel components.
    seq.pack(side=BOTTOM)

    return tk


if __name__ == '__main__':
    ''' Loads synthesizer and starts graphical interface. '''

    synthesizer = Synth.synth()

    tk = setup(synthesizer)

    tk.mainloop()
