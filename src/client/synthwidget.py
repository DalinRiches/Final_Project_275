import tkinter
from tkinter.constants import *

import dialwidget
import graphwidget

PANEL_HEIGHT = 100
PANEL_WIDTH = 256
PANEL_GS_HEIGHT = 64
PANEL_GS_WIDTH = PANEL_WIDTH
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

        # graph screen
        self.w_graph = graphwidget.GraphScreen(
            parent=self.w_mid,
            width=PANEL_GS_WIDTH,
            height=PANEL_GS_HEIGHT,
            fx=self._graph_fx
        )

        self.w_graph.pack(side=TOP)

        # special init
        self._special_init()

        # dials
        self._dial_targets = dict()
        for dial in self._dials():
            self._add_dial(**dial)

        # Toggle from False to True for consistency
        self._toggle_enabled()


    def _special_init(self):
        ''' Subclasses can override this to set up specific
        widgets without having to modify __init__ itself. It
        is called just before the dials are generated. '''
        pass


    def _dials(self):
        ''' This should be overridden on subclasses to specify
        exactly what dials should be created. This function
        should return a list of dictionaries, each one specifying
        the parameters of a Dial plus the identifier (as a string)
        of a target parameter that the dial should set. (see _add_dial) '''
        pass


    def _graph_fx(self, x):
        ''' This is the function that will be displayed on the graph.
        It should be overridden in each subclass by a function that
        takes an integer and returns an integer. '''
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
                  "Only the callback will function.".format(
                    kwargs['label'], self._label))

        # convert targets to callbacks
        if 'callback' not in kwargs and 'target' in kwargs:
            kwargs['callback'] = self._set_param
            target = kwargs['target']

            if target not in self.target.__dict__:
                print("*** SynthPanel WARNING: Dial {} of widget {} "
                      "targets parameter {} of {}, which doesn't look "
                      "like it exists.".format(
                        kwargs['label', self._label, target, self.target]))

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
        self.target.enable = self.enabled


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

    _label = "Oscillator"

    def _dials(self):
        return [
            {'label': "Waveshape",
             'dmin': 0, 'dmax': 6, 'dincrement': 1,
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
             'target': 'detune' }
        ]


    def _graph_fx(self, x):
        wtx = self.target.wavetablepos + ((2048 * x) // PANEL_GS_WIDTH)
        wtval = (self.target.wave_tables[wtx] + 32768) % 65536
        return PANEL_GS_HEIGHT * wtval // 65536


    def _set_waveshape(self, value, label):
        self.target.wavetablepos = int(value + 0.001) * 2048
        self.w_graph.redraw()


class EnvPanel(SynthPanel):
    ''' SynthPanel for an Envelope component. '''

    _label = "Envelope"


    def _special_init(self):
        self._val_atk = 0.07
        self._val_dec = 0.08
        self._val_sus_time = 0.15
        self._val_sus_lvl = 0.8
        self._val_rel = 0.1


    def _dials(self):
        return [
            {'label': "Attack",
             'dmin': 0, 'dmax': 2,
             'dinitial': self._val_atk,
             'callback': self._set_adr },
            {'label': "Decay",
             'dmin': 0, 'dmax': 2,
             'dinitial': self._val_dec,
             'callback': self._set_adr },
            {'label': "Sustain",
             'dmin': 0, 'dmax': 2,
             'dinitial': self._val_sus_time,
             'callback': self._set_sustain },
            {'label': "Sus. Level",
             'dmin': 0, 'dmax': 1,
             'dmintext': "0.0", 'dmaxtext': "1.0",
             'dinitial': self._val_sus_lvl,
             'callback': self._set_sustain },
            {'label': "Release",
             'dmin': 0, 'dmax': 2,
             'dinitial': self._val_rel,
             'callback': self._set_adr }
        ]


    def _graph_fx(self, x):
        t = ((0.5 * x / PANEL_GS_WIDTH) * self.target.samplerate)
        envval = self.target.gen_env(t, 1)
        return int(envval * (PANEL_GS_HEIGHT - 4))


    def _set_adr(self, value, label):
        if label == "Attack":
            self.target.set_attack(value)
        elif label == "Decay":
            self.target.set_decay(value)
        elif label == "Release":
            self.target.set_release(value)

        self.w_graph.redraw()


    def _set_sustain(self, value, label):
        if label == "Sustain":
            self._val_sus_time = value
        elif label == "Sus. Level":
            self._val_sus_lvl = value

        self.target.set_sustain(self._val_sus_time, self._val_sus_lvl)
        self.w_graph.redraw()


class FiltPanel(SynthPanel):
    ''' SynthPanel for a Filter component. '''

    _label = "Filter"

    def _special_init(self):
        self.band = "Low Pass"
        self._last_value = -5

        # Low-pass/High-pass toggle
        self.w_band = tkinter.Button(
            self.w_bot,
            text="###",
            justify=CENTER,
            font=PANEL_FONT+" 9",
            command=self._toggle_band
        )
        self.w_band.pack(side=LEFT, fill=X, padx=3)

        self._toggle_band()


    def _toggle_band(self):
        if self.band == "Low Pass":
            self.w_band.config(text="HIGH", bg="darkcyan")
            self.band = "High Pass"
            self._log_set_cutoff(self._last_value, None)
        else:
            self.w_band.config(text=" LOW", bg="blue")
            self.band = "Low Pass"
            self._log_set_cutoff(self._last_value, None)


    def _dials(self):
        return [
            {'label': "Cutoff",
             'dmin':-5, 'dmax':5, # (logarithmic scaled)
             'dmintext':"E-5", 'dmaxtext':"E+5",
             'dinitial': -5,
             'callback': self._log_set_cutoff}
        ]


    def _graph_fx(self, x):
        return PANEL_GS_HEIGHT/2


    def _log_set_cutoff(self, value, label):
        print("Setting to {}, cutoff = {}".format(self.band, 10**value))
        self._last_value = value
        if self.band == "High Pass":
            self.target.set_cutoff_highpass(10**value)
        else:
            self.target.set_cutoff_lowpass(10**value)


class LFOPanel(SynthPanel):
    pass
