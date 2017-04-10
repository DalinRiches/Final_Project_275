import tkinter
from tkinter.constants import *

import dialwidget
import graphwidget

''' Synthesizer controller widgets:
        Selector - radio button bar
        OscController - visual oscillator controller
'''


class _SelElem:
    ''' Selector Bar Element - class representing a single
    element of a Selector bar. Encapsulates a button widget
    which calls the parent's callback function when pressed.
    (See synthwidgets.Selector for more information)
    
    Parameters:
        sel_parent: (Selector) the selector this step is a member of.
        idx: (int) index of this element in the selector.
        text: (str) text to appear on the encapsulated button.
    '''
        
    def __init__(self, sel_parent, idx, text):
        ''' Initializer for _SelElem (see class documentation)'''
        # regular data
        self.sel_parent = sel_parent
        self.idx = idx
        
        # encapsulated widget
        self.widget = tkinter.Button(
            sel_parent.widget,
            text=text,
            font="Fixed 9",
            command=self._parent_select
        )
        
        # set to deselected by default, for consistency
        self.deselect()
        
        # automatically pack encapsulated widget left to right
        # (NOTE in a really complete implementation, one
        #  could imagine Selectors pointing in different
        #  directions (top to bottom, right to left...)
        #  created by parameterizing this packing)
        self.widget.pack(side=LEFT)
    
    
    def select(self):
        ''' Visually sets this step to selected. '''
        self.widget.config(bg='blue')
    
    
    def deselect(self):
        ''' Visually sets this step to deselected. '''
        self.widget.config(bg='black')
    
    def _parent_select(self):
        ''' Calls parent callback with this element's index. '''
        self.sel_parent._select(self.idx)
    


class Selector:
    ''' Selector Bar Widget - a radio-button style selector bar.
    
    Parameters:
        parent: (Widget) tk-style parent widget.
        elements: (list[str]) (or anything convertible to str)
            Elements of the selector. Each element will appear
            as a button in the selector with the specified text.
        callback: (function) will be called when an element
            is selected, passing the index of the element. None
            can be specified for no callback.
        init_idx: (int) index of the initially selected element.
            Default 0.
    '''
    
    def __init__(self, parent, elements, callback=None, init_idx=0):
        ''' Initializer for Selector (see class documentation)'''
        # regular data
        self.parent = parent
        self.callback = callback
        
        # encapsulated widget
        self.widget = tkinter.Frame(parent)
        
        # elements
        self.elements = [_SelElem(self, i, str(s))
                         for i, s in enumerate(elements)]
        
        # start with an element selected
        self._selected = init_idx
        self.elements[init_idx].select()
    
    
    def pack(self, **kwargs):
        ''' Packs the encapsulated widget.
        
        Arguments:
            same as underlying pack() function.
        '''
        
        self.widget.pack(**kwargs)
    
    
    def _select(self, idx):
        ''' Called by the elements of the selector when clicked.
        Sets the appropriate selected/deselected states and
        calls the callback function. '''
        
        self.elements[self._selected].deselect()
        self._selected = idx
        self.elements[idx].select()
        
        if self.callback is not None:
            self.callback(idx)
    

# TODO could OscController and EnvController be turned into
# subclasses of one ComponentController class?

class OscController:
    def __init__(self, parent, oscillator, waveshape, volume, detune):
        # regular data
        self.waveshape = waveshape
        self.volume = volume
        self.detune = detune
        self.enabled = False
        self.oscillator = oscillator
        
        # encapsulated widget
        self.widget = tkinter.Frame(parent, bd=1, relief=RAISED, pady=3,
            padx=3)
        ### self.widget.pack(side=LEFT)
        
        
        # individual controls
        
        # The top frame contains the label and toggle
        self.w_top_frame = tkinter.Frame(self.widget, pady=5)
        
        # top frame --> label
        self.w_label = tkinter.Label(
            self.w_top_frame,
            text="Oscillator",
            font="Fixed 8",
            padx=5
        )
        
        # top frame --> disable-completely toggle
        self.w_toggle = tkinter.Button(
            self.w_top_frame,
            font="Fixed 9",
            command=self.toggle_enabled
        )
        
        # pack top frame
        self.w_label.pack(side=RIGHT, expand=1)
        self.w_toggle.pack(side=LEFT)
        self.w_top_frame.pack(side=TOP)
        
        # Middle frame: waveshape selector
        self.w_mid_frame = tkinter.Frame(self.widget)
        
        # bottom frame --> graphview
        self.w_waveview = graphwidget.GraphWidget()
        
        # Bottom frame: controls (waveshape, volume, detune)
        self.w_bot_frame = tkinter.Frame(self.widget)
        
        # bottom frame --> waveshape dial
        # TODO read number of waveshapes
        self.w_waveshape = dialwidget.Dial(
            self.w_bot_frame,
            text="Waveshape",
            dmin=0,
            dmax=16,
            dinitial=0,
            dincrement=1,
            callback=self.set_waveshape
        )
        
        # bottom frame --> volume dial
        self.w_volume = dialwidget.Dial(
            self.w_bot_frame,
            text="Volume",
            dmin=0.0,
            dmax=1.0,
            dinitial=1.0,
            dmintext='0%',
            dmaxtext='100%',
            callback=self.set_volume
        )
        
        # bottom frame --> detune dial
        self.w_detune = dialwidget.Dial(
            self.w_bot_frame,
            text="Detune",
            dmin=-24,
            dmax=24,
            dinitial=0,
            dmintext='-24',
            dmaxtext='+24',
            callback=self.set_detune
        )
        self.w_waveshape.pack(side=LEFT)
        self.w_volume.pack(side=LEFT)
        self.w_detune.pack(side=LEFT)
        self.w_bot_frame.pack(side=TOP)
        
        # starts FALSE, set TRUE
        self.toggle_enabled()
    
    
    def toggle_enabled(self):
        if self.enabled:
            self.w_toggle.config(text="OFF", bg="red")
        else:
            self.w_toggle.config(text=" ON", bg="green")
        self.enabled = not self.enabled
    
    
    def set_waveshape(self, value):
        # (correcting for float error)
        self.waveshape = int(value+0.001)
    
    
    def set_detune(self, value):
        self.detune = value
    
    
    def set_volume(self, value):
        self.volume = value
    
    
    def apply(self):
        ''' Applies the settings to the underlying oscillator. '''
        if not self.enabled:
            self.oscillator.volume = 0.0
        else:
            # TODO set waveshape
            self.oscillator.volume = self.volume
            self.oscillator.detune = self.detune
    
    def pack(self, **kwargs):
        self.widget.pack(**kwargs)
    

class EnvController:
    def __init__(self, parent, envelope, adsr):
        # regular data
        self.parent = parent
        self.envelope = envelope
        self.adsr = adsr
        self.enabled = False
        
        self.widget = tkinter.Frame(parent, bd=1, relief=RAISED, pady=3,
            padx=3)
        self.widget.pack(side=LEFT)
        
        
        # individual controls
        
        # The top frame contains the label and toggle
        self.w_top_frame = tkinter.Frame(self.widget, pady=5)
        
        # top frame --> label
        self.w_label = tkinter.Label(
            self.w_top_frame,
            text="Envelope",
            font="Fixed 8",
            padx=5
        )
        
        # top frame --> disable-completely toggle
        self.w_toggle = tkinter.Button(
            self.w_top_frame,
            font="Fixed 9",
            command=self.toggle_enabled
        )
        
        # pack top frame
        self.w_label.pack(side=RIGHT, expand=1)
        self.w_toggle.pack(side=LEFT)
        self.w_top_frame.pack(side=TOP)
        
        # Middle frame: form viewer
        self.w_mid_frame = tkinter.Frame(self.widget)
        
        # middle frame --> graphview
        self.w_waveview = graphwidget.GraphWidget()
        
        # Bottom frame: controls (ADSR)
        self.w_bot_frame = tkinter.Frame(self.widget)
        
        # bottom frame --> attack time
        self.w_atk = dialwidget.Dial(
            self.w_bot_frame,
            text="Attack",
            dmin=0,
            dmax=2,
            dinitial=0.2,
            callback=self.set_atk
        )
        
        # bottom frame --> decay time
        self.w_dec = dialwidget.Dial(
            self.w_bot_frame,
            text="Decay",
            dmin=0,
            dmax=2,
            dinitial=0.4,
            callback=self.set_dec
        )
        
        # bottom frame --> sustain level
        self.w_sus = dialwidget.Dial(
            self.w_bot_frame,
            text="Sustain",
            dmin=0.0,
            dmax=1.0,
            dinitial=0.0,
            dmintext='0.0',
            dmaxtext='1.0',
            callback=self.set_sus
        )
        
        # bottom frame --> release time
        self.w_rel = dialwidget.Dial(
            self.w_bot_frame,
            text="Release",
            dmin=0,
            dmax=2,
            dinitial=0.05,
            callback=self.set_rel
        )
        
        self.w_atk.pack(side=LEFT)
        self.w_sus.pack(side=LEFT)
        self.w_dec.pack(side=LEFT)
        self.w_rel.pack(side=LEFT)
        self.w_bot_frame.pack(side=TOP)
        
        # starts FALSE, set TRUE
        self.toggle_enabled()
    
    def toggle_enabled(self):
        if self.enabled:
            self.w_toggle.config(text="OFF", bg="red")
        else:
            self.w_toggle.config(text=" ON", bg="green")
        self.enabled = not self.enabled
    
    
    def set_atk(self, value):
        self.adsr[0] = value
    
    def set_dec(self, value):
        self.adsr[1] = value
    
    def set_sus(self, value):
        self.adsr[2] = value
    
    def set_rel(self, value):
        self.adsr[3] = value
    
    def pack(self, **kwargs):
        self.widget.pack(**kwargs)
    
    def apply(self):
        self.envelope.enabled = self.enabled
        (self.envelope.attack, self.envelope.decay,
            self.envelope.sustain, self.envelope.release) = self.adsr
