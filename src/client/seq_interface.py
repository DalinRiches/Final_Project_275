# For graphics
import tkinter
from tkinter.constants import *

# Custom widget-like definitions
import synthwidgets

# Synthesizer
import Synth






''' The current step of the sequence. '''
current_step = 0


def set_step(idx):
    ''' Sets the current step of the sequence to show in the
    oscillator interface. '''

    print("Displaying step {}".format(idx))
    current_step = idx

def setup(synth):
    ''' Sets up the interface and returns a reference to
    the base Tk widget. '''

    tk = tkinter.Tk()

    # main sequence bar
    mainseq = synthwidgets.Selector(
        parent=tk,
        elements=["{:02d}".format(i) for i in range(16)],
        callback=set_step
    )
    mainseq.pack(side=BOTTOM)

    osc1ct = synthwidgets.OscController(
        parent=tk,
        oscillator=synth.oscil,
        volume=0.75,
        offset=0,
        detune=0
    )
    osc2ct = synthwidgets.OscController(
        parent=tk,
        oscillator=synth.oscil2,
        volume=0.75,
        offset=0,
        detune=0
    )


    return tk


if __name__ == '__main__':
    synthesizer = Synth.synth()

    tk = setup(synthesizer)

    tk.mainloop()
