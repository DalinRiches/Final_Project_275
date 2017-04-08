# For graphics
import tkinter
from tkinter.constants import *

# Custom widget-like definitions
import synthwidget
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
        self.synth.play(seq, slide=True)
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
    
    # TODO: This would probably look better with the grid()
    # geometry manager if I can figure out how to do that...
    
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
    
    # osc1ct = synthwidgets.OscController(
    #     parent=oscframe,
    #     oscillator=synth.oscil,
    #     volume=0.75,
    #     waveshape=0,
    #     detune=0
    # )
    # osc2ct = synthwidgets.OscController(
    #     parent=oscframe,
    #     oscillator=synth.oscil2,
    #     volume=0.75,
    #     waveshape=0,
    #     detune=0
    # )
    
    osc1ct = synthwidget.OscPanel(
        parent=oscframe,
        target=synth.oscil
    )
    osc2ct = synthwidget.OscPanel(
        parent=oscframe,
        target=synth.oscil2
    )
    # filt1ct = synthwidget.FiltPanel(
    #     parent=oscframe,
    #     target=synth.fil1
    # )
    
    # ctrl.bind(osc1ct.apply)
    # ctrl.bind(osc2ct.apply)
    osc1ct.pack(side=LEFT, fill=X)
    osc2ct.pack(side=LEFT, fill=X)
    # filt1ct.pack(side=LEFT, fill=X)
    oscframe.pack(side=TOP, fill=X)
    
    envframe = tkinter.Frame()
    
    # env1ct = synthwidgets.EnvController(
    #     parent=envframe,
    #     envelope=synth.env1,
    #     adsr=[0.1, 0.2, 0.9, 0.1]
    # )
    # env2ct = synthwidgets.EnvController(
    #     parent=envframe,
    #     envelope=synth.env2,
    #     adsr=[0.1, 0.2, 0.9, 0.1]
    # )
    env1ct = synthwidget.EnvPanel(
        parent=envframe,
        target=synth.env1
    )
    env2ct = synthwidget.EnvPanel(
        parent=envframe,
        target=synth.env2
    )
    # filt2ct = synthwidget.FiltPanel(
    #     parent=envframe,
    #     target=synth.fil2
    # )
    
    # panelframe.grid()
    # osc1ct.grid(column=0, row=0)
    # osc2ct.grid(column=1, row=0)
    # env1ct.grid(column=0, row=1)
    # env2ct.grid(column=1, row=1)
    
    # ctrl.bind(env1ct.apply)
    # ctrl.bind(env2ct.apply)
    env1ct.pack(side=LEFT, fill=X)
    env2ct.pack(side=LEFT, fill=X)
    # filt2ct.pack(side=LEFT, fill=X)
    envframe.pack(side=TOP, fill=X)
    
    ctrlbar = gen_controlbar(tk, ctrl)
    ctrlbar.pack(side=BOTTOM)
    
    return tk


if __name__ == '__main__':
    synthesizer = Synth.synth()
    
    tk = setup(synthesizer)
    
    tk.mainloop()
