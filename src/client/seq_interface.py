# For graphics
import tkinter
from tkinter.constants import *

# Custom widget-like definitions
import synthwidgets
import seqwidget

# Synthesizer
import synth





def gen_controlbar(tk, synth, seq):
    def _play_sequence():
        print("Playing sequence")
        sequence = seq.sequence()
        print("Sequence is:\n{}".format(sequence))
        synth.play(sequence)
        print("Done")
    
    bar = tkinter.Frame(
        tk,
        bd=2,
        relief=RAISED
    )
    
    bar_play = tkinter.Button(
        bar,
        bg="green",
        text="Play",
        command=_play_sequence
    )
    bar_play.pack(side=LEFT)
    
    return bar


# ''' The current step of the sequence. '''
# current_step = 0
#
#
# def set_step(idx):
#     ''' Sets the current step of the sequence to show in the
#     oscillator interface. '''
#
#     print("Displaying step {}".format(idx))
#     current_step = idx

def setup(synth):
    ''' Sets up the interface and returns a reference to
    the base Tk widget. '''
    
    tk = tkinter.Tk()
    
    # main sequence bar
    # mainseq = synthwidgets.Selector(
    #     parent=tk,
    #     elements=["{:02d}".format(i) for i in range(16)],
    #     callback=set_step
    # )
    # mainseq.pack(side=BOTTOM)
    
    seq = seqwidget.Sequencer(
        parent=tk,
        length=32,
        height=24
    )
    seq.pack(side=BOTTOM)
    
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
    
    ctrlbar = gen_controlbar(tk, synth, seq)
    ctrlbar.pack(side=BOTTOM)
    
    return tk


if __name__ == '__main__':
    synthesizer = synth.synth()
    
    tk = setup(synthesizer)
    
    tk.mainloop()
