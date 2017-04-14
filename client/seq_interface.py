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
    seqsource contains a function that generates a sequence of notes.

    Parameters:
        synth: (Synth) the synthesizer object that the controller controls

    Note that self.seqsource should be set after this class's instantiation
    for playback to actually work.
    '''

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


    def start(self):
        ''' Invokes the synthesizer to start rendering the sequence available
        in seqsource. '''
        seq = self.get_sequence()
        print("Rendering...")
        self.synth.play(seq)
        print("Done.")


    def toggle_record(self):
        '''Sets synth.record. '''
        self.synth.record = not(self.synth.record)
        self._toggle_msg(self.synth.record, "Recording")


    def toggle_playback(self):
        '''Sets synth.playback. '''
        self.synth.playback = not(self.synth.playback)
        self._toggle_msg(self.synth.playback, "Playback")


    def _toggle_msg(self, target, label):
        ''' Prints a message indicating toggle state. '''
        i=['De-activated','Activated']
        print("{} is now: {}".format(label, i[target]))



def gen_controlbar(tk, ctrl):
    ''' Creates the main playback control bar, with a Play button
    and a speed (reciprocal tempo) dial. '''

    def _toggle_record():
        ''' Callback function for the recording toggle. '''
        ctrl.toggle_record()
        _update_button(bar2_rec, ctrl.synth.record)


    def _toggle_playback():
        ''' Callback function for the playback toggle. '''
        ctrl.toggle_playback()
        _update_button(bar2_play, ctrl.synth.playback)


    def _update_button(button, target):
        if target:
            button.configure(bg="gray75")
        else:
            button.configure(bg="gray50")


    panel = tkinter.Frame(
        tk,
        relief=RAISED,
        bg="black",
        bd=0,
        highlightthickness=0,
    )

    bar1 = tkinter.Frame(
        panel,
        relief=RAISED,
        bg="black",
        bd=0,
        highlightthickness=0,
    )

    bar1_dial = dialwidget.Dial(
        bar1,
        label="Speed",
        dmin=0.2, dmax=2.0,
        dinitial=0.5,
        callback=ctrl.set_play_speed
    )

    bar1_render = tkinter.Button(
        bar1,
        bg="green",
        text="Render",
        font="Fixed 9",
        command=ctrl.start,
        bd=1,
        highlightthickness=0,
    )
    bar2 = tkinter.Frame(
        panel,
        relief=RAISED,
        bg="black",
        bd=0,
        highlightthickness=0,
    )

    bar2_rec = tkinter.Button(
        bar2,
        bg="gray50",
        text="Record",
        font="Fixed 9",
        command=_toggle_record,
        bd=1,
        highlightthickness=0,
    )

    bar2_play = tkinter.Button(
        bar2,
        bg="gray50",
        text="Playback",
        font="Fixed 9",
        command=_toggle_playback,
        bd=1,
        highlightthickness=0,
    )


    bar1_dial.pack(side=LEFT, pady=3, padx=3)
    bar1_render.pack(side=LEFT, expand=1, pady=3,padx=3)
    bar2_play.pack(side=LEFT, expand=1,pady=3,padx=3)
    bar2_rec.pack(side=LEFT, expand=1,pady=3,padx=3)
    bar1.pack(side=BOTTOM, expand=1)
    bar2.pack(side=BOTTOM, expand=1)

    # consistency
    _update_button(bar2_play, ctrl.synth.playback)
    _update_button(bar2_rec, ctrl.synth.record)

    return panel


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
        temposource=ctrl.get_play_speed,
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
        target=synth.oscil,
    )
    osc2ct = synthwidgets.OscPanel(
        parent=oscframe,
        target=synth.oscil2,
    )
    filt1ct = synthwidgets.FiltPanel(
        parent=oscframe,
        target=synth.fil1,
    )

    osc1ct.pack(side=LEFT, fill=X, padx=5, pady=5)
    osc2ct.pack(side=LEFT, fill=X, padx=5, pady=5)
    filt1ct.pack(side=LEFT, fill=X, padx=5, pady=5)
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

    env1ct.pack(side=LEFT, fill=X, padx=5, pady=5)
    env2ct.pack(side=LEFT, fill=X, padx=5, pady=5)
    filt2ct.pack(side=LEFT, fill=X, padx=5, pady=5)
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

    lfo1ct.pack(side=LEFT, fill=X, padx=5, pady=5)
    lfo2ct.pack(side=LEFT, fill=X, padx=5, pady=5)
    lfo3ct.pack(side=LEFT, fill=X, padx=5, pady=5)
    lfoframe.pack(side=TOP)


    # Playback panel
    ctrlbar = gen_controlbar(tk, ctrl)
    ctrlbar.pack(side=RIGHT, fill=X, expand=1, anchor=N)


    # NOTE seq must be packed last so that if the window runs
    # out of room it loses seq rows, instead of more important
    # things like panel components.
    seq.pack(side=BOTTOM, padx=5, pady=5)

    return tk


if __name__ == '__main__':
    ''' Loads synthesizer and starts graphical interface. '''

    synthesizer = Synth.synth()

    tk = setup(synthesizer)

    tk.mainloop()
