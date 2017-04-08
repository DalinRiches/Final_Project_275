# For graphics
import tkinter
from tkinter.constants import *

# Custom widget-like definitions
import synthwidgets
import seqwidget

# Synthesizer
import Synth



class PlaybackController:
    ''' Contains a synth object and a list of callbacks.
    When play() is called, all the callbacks are invoked
    in the order they were bound before calling play on
    the synth object. Used to apply changes from the
    interface. '''
    
    def __init__(self, synth):
        self.synth = synth
        self.callbacks = []
        self.seq_callback = None
        self.seq = None
    
    
    def bind(self, fn):
        self.callbacks.append(fn)
    
    
    def bind_seq_generator(self, fn):
        self.seq_callback = fn
    
    
    def get_sequence(self):
        print("Getting sequence...")
        seq = self.seq_callback()
        print(seq)
        return seq
    
    
    def play(self):
        for fn in self.callbacks:
            fn()
        
        seq = self.get_sequence()
        print("Playing...")
        self.synth.play(seq)
        print("Done")
        
    

def gen_controlbar(tk, ctrl):
    bar = tkinter.Frame(
        tk,
        bd=2,
        relief=RAISED
    )
    
    bar_play = tkinter.Button(
        bar,
        bg="green",
        text="Play",
        command=ctrl.play
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
    
    ctrl = PlaybackController(synth)
    
    tk = tkinter.Tk()
    
    seq = seqwidget.Sequencer(
        parent=tk,
        length=32,
        height=24
    )
    seq.pack(side=BOTTOM)
    
    ctrl.bind_seq_generator(seq.sequence)
    
    oscframe = tkinter.Frame()
    
    osc1ct = synthwidgets.OscController(
        parent=oscframe,
        oscillator=synth.oscil,
        volume=0.75,
        waveshape=0,
        detune=0
    )
    osc2ct = synthwidgets.OscController(
        parent=oscframe,
        oscillator=synth.oscil2,
        volume=0.75,
        waveshape=0,
        detune=0
    )
    
    ctrl.bind(osc1ct.apply)
    ctrl.bind(osc2ct.apply)
    osc1ct.pack(side=LEFT)
    osc2ct.pack(side=RIGHT)
    oscframe.pack(side=TOP)
    
    envframe = tkinter.Frame()
    
    env1ct = synthwidgets.EnvController(
        parent=envframe,
        envelope=synth.env1,
        adsr=[0.1, 0.2, 0.9, 0.1]
    )
    env2ct = synthwidgets.EnvController(
        parent=envframe,
        envelope=synth.env2,
        adsr=[0.1, 0.2, 0.9, 0.1]
    )
    
    ctrl.bind(env1ct.apply)
    ctrl.bind(env2ct.apply)
    env1ct.pack(side=LEFT)
    env2ct.pack(side=RIGHT)
    envframe.pack(side=TOP)
    
    ctrlbar = gen_controlbar(tk, ctrl)
    ctrlbar.pack(side=BOTTOM)
    
    return tk


if __name__ == '__main__':
    synthesizer = Synth.synth()
    
    tk = setup(synthesizer)
    
    tk.mainloop()
