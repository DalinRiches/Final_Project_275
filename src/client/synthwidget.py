import tkinter
from tkinter.constants import *

import dialwidget
import graphwidget

PANEL_HEIGHT = 100
PANEL_WIDTH = 120
PANEL_FONT = "Fixed"

class SynthPanel:
    ''' Base control panel widget. Every control panel has three panels:
    a Top panel, containing a label and a toggle;
    a Middle panel, containing a graphscreen (optional);
    and a Bottom panel, containing some Dials.
    
    Parameters:
        parent: (Widget) tk-style parent widget
        target: (Synth component) the component to control
    
    This is a base class. It should not be directly placed on screen.
    Instead, the subclasses OscPanel, EnvPanel, FiltPanel, and LFOPanel
    should be used. '''
    
    ''' Override this to change the label on the panel '''
    _label = "Panel"
    
    def __init__(self, parent, target):
        # regular data
        self.target = target
        self.enabled = False
        
        # encapsulated widget
        self.widget = tkinter.Frame(
            parent,
            height=PANEL_HEIGHT,
            width=PANEL_WIDTH,
            bd=2,
            relief=RAISED
        )
        
        # three panels
        self.w_top, self.w_mid, self.w_bot = (tkinter.Frame(
            self.widget,
            width=PANEL_WIDTH,
            bd=0
        ) for _ in range(3))
        
        self.w_top.pack(side=TOP, fill=BOTH)
        self.w_mid.pack(side=TOP, fill=BOTH)
        self.w_bot.pack(side=TOP, fill=BOTH)
        
        # label and toggle
        self.w_label = tkinter.Label(
            self.w_top,
            text=self._label,
            justify=CENTER,
            font=PANEL_FONT+" 9"
        )
        self.w_toggle = tkinter.Button(
            self.w_top,
            text="###",
            justify=CENTER,
            font=PANEL_FONT+" 9",
            command=self._toggle_enabled
        )
        
        self.w_toggle.pack(side=LEFT)
        self.w_label.pack(side=LEFT, fill=BOTH, padx=5)
        
        # graph screen (TODO)
        self.w_graph = graphwidget.GraphScreen(
            parent=self.w_mid
        )
        
        self.w_graph.pack(side=TOP)
        
        # dials
        self._dial_targets = dict()
        for dial in self._dials():
            self._add_dial(**dial)
        
        # Toggle from False to True for consistency
        self._toggle_enabled()
    
    
    def _dials(self):
        ''' This should be overridden on subclasses to specify
        exactly what dials should be created. This function
        should return a list of dictionaries, each one specifying
        the parameters of a Dial plus the identifier (as a string)
        of a target parameter that the dial should set. (see _add_dial) '''
        pass
    
    
    def _add_dial(self, **kwargs):
        # make sure this dial actually does something
        if 'callback' not in kwargs and 'target' not in kwargs:
            print("*** SynthPanel WARNING: Dial {} of widget {} "
                  "does not target a parameter or specify a callback "
                  "and will therefore be completely useless.".format(
                    kwargs['label'], self._label))
        
        # but not two conflicting things
        if 'callback' in kwargs and 'target' in kwargs:
            print("*** SynthPanel WARNING: Dial {} of widget {} "
                  "specifies both target parameter and callback. "
                  "Only the callback will function.")
        
        # convert targets to callbacks
        if 'callback' not in kwargs and 'target' in kwargs:
            kwargs['callback'] = self._set_param
            target = kwargs['target']
            del kwargs['target']
        else:
            target = None
        
        # save target
        self._dial_targets[kwargs['label']] = target
        
        # instantiate dial
        dial = dialwidget.Dial(
            parent=self.w_bot,
            **kwargs
        )
        dial.pack(side=LEFT, expand=1)
    
    
    def _toggle_enabled(self):
        if self.enabled:
            self.w_toggle.config(text="OFF", bg="red")
        else:
            self.w_toggle.config(text=" ON", bg="green")
        self.enabled = not self.enabled
        self.target.enabled = self.enabled
    
    
    def _set_param(self, value, label):
        ''' Sets the parameter named by _dial_targets[label]
        (set up by _add_dial) to the value. This is a callback
        function which will be called by a Dial widget. '''
        iden = self._dial_targets[label]
        self.target.__dict__[iden] = value
    
    
    def pack(self, **kwargs):
        ''' Packs the underlying widget. '''
        self.widget.pack(**kwargs)
    
    
    def grid(self, **kwargs):
        ''' Grid-places the underlying widget. '''
        self.widget.grid(**kwargs)


class OscPanel(SynthPanel):
    ''' SynthPanel for an Oscillator component. '''
    
    def _dials(self):
        return [
            {'label': "Waveshape",
             'dmin': 0, 'dmax': 15, 'dincrement': 1,
             'dinitial': 0,
             'callback': self._set_waveshape },
            {'label': "Volume",
             'dmin': 0.0, 'dmax': 1.0,
             'dmintext': "0%", 'dmaxtext': "100%",
             'dinitial': 0.75,
             'target': 'volume' },
            {'label': "Detune",
             'dmin': -24, 'dmax': 24,
             'dmintext': "-24", 'dmaxtext': "+24",
             'dinitial': 0,
             'target': 'detune'}
        ]
    
    def _set_waveshape(self, value, label):
        # TODO still don't know how to set waveshapes.
        pass


class EnvPanel(SynthPanel):
    ''' SynthPanel for an Envelope component. '''
    
    _label = "Envelope"
    
    def _dials(self):
        return [
            {'label': "Attack",
             'dmin': 0, 'dmax': 2,
             'dinitial': 0.1,
             'target': 'attack'},
            {'label': "Decay",
             'dmin': 0, 'dmax': 2,
             'dinitial': 0.2,
             'target': 'decay'},
            {'label': "Sustain",
             'dmin': 0, 'dmax': 1,
             'dmintext': "0.0", 'dmaxtext': "1.0",
             'dinitial': 0.8,
             'target': 'sustain_amp'},
            {'label': "Release",
             'dmin': 0, 'dmax': 2,
             'dinitial': 0.2,
             'target': 'release'}
        ]


class FiltPanel(SynthPanel):
    ''' SynthPanel for a Filter component. '''
    pass

class LFOPanel(SynthPanel):
    pass
