import osc, wavetables

# For graphics
import tkinter
from tkinter.constants import *


class dialwidget:
    def __init__(self, parent, dmin, dmax, dinitial,
            text, callback, dmintext=None, dmaxtext=None, incr=None):
        # Basic parameters: minimum, maximum, initial values
        self.dmin = dmin
        self.dmax = dmax
        self.dinitial = dinitial
        
        # Text: main label, min value text, max value text
        self.text = text
        
        # If no min/max labels specified, use values
        if dmintext is None:
            self.dmintext = str(self.dmin)
        else:
            self.dmintext = dmintext
        if dmaxtext is None:
            self.dmaxtext = str(self.dmax)
        else:
            self.dmaxtext = dmaxtext
        
        # Current value and mouse-click state
        self.value = dinitial
        self.dragging = False
        
        # Increment - calculate increment angle as well
        if incr is not None:
            from math import pi
            self.incr = incr
            self.incr_angle = (3*pi/2) / ((dmax - dmin)/incr)
        else:
            self.incr = None
            self.incr_angle = None
        
        # Callback - function to call when value changes
        self.callback = callback
        
        # Create Tkinter widget
        self.widget = tkinter.Canvas(parent, width=50, height=50,
            relief=FLAT
        )
        
        # Subitems of widget:
        # Main text label
        self.wd_label = self.widget.create_text(
            25, 6, justify="center", fill="white", font="Fixed 6", text=text)
        # Min value label
        self.wd_minlabel = self.widget.create_text(
            25-15-3, 30+15, justify="right", fill="white", font="Fixed 4",
            text=self.dmintext
        )
        # Max value label
        self.wd_maxlabel = self.widget.create_text(
            25+15+3, 30+15, justify="left", fill="white", font="Fixed 4",
            text=self.dmaxtext
        )
        # Dial body
        self.wd_circle = self.widget.create_oval(
            25-15, 30-15, 25+15, 30+15, outline="white", fill="white",
            stipple="gray25")
        # Dial body events: click/move/release to change,
        # double-click to reset
        self.widget.bind('<Button-1>', self.mouse_down)
        self.widget.bind('<Double-Button-1>', self.mouse_dbl)
        self.widget.bind('<Motion>', self.mouse_handle)
        self.widget.bind('<ButtonRelease-1>', self.mouse_up)
        # Dial pointer
        self.wd_indic = self.widget.create_line(25, 30-15, 25, 30-10,
            fill="white")
        
        # Initialize pointer location and callback
        self.set_value_by_angle(self.val_to_angle(dinitial))
    
    def angle_to_val(self, angle):
        # converting (-3pi/4) <--> (3pi/4) to (MIN) <--> (MAX)
        from math import pi
        value = ((angle * (self.dmax - self.dmin) * 4 / (3 * pi))
                + self.dmax + self.dmin) / 2
        return value
    
    def val_to_angle(self, value):
        from math import pi
        angle = ((3 * pi * (2 * value - (self.dmax + self.dmin)))
                / (4 * (self.dmax - self.dmin)))
        return angle
    
    def set_value_by_angle(self, angle):
        from math import sin, cos, pi
        xr = cos(angle - (pi/2))
        yr = sin(angle - (pi/2))
        
        x1 = 25 + (15 * xr)
        y1 = 30 + (15 * yr)
        x2 = 25 + (5 * xr)
        y2 = 30 + (5 * yr)
        
        self.widget.coords(self.wd_indic, x1, y1, x2, y2)
        
        self.value = self.angle_to_val(angle)
        self.callback(self.value)
    
    def mouse_dbl(self, ev):
        self.set_value_by_angle(self.val_to_angle(self.dinitial))
    
    def mouse_down(self, ev):
        self.dragging = True
    
    def mouse_up(self, ev):
        self.dragging = False
    
    def mouse_handle(self, ev):
        if self.dragging:
            from math import atan2, pi
            angle = atan2(ev.y - 30, ev.x - 25) + (pi/2)
            if angle > pi:
                angle -= 2*pi
            angle = min(3*pi/4, max(angle, -3*pi/4))
            if self.incr_angle is not None:
                # round to nearest multiple of incr_angle
                angle = (round((angle + (3*pi/4)) / self.incr_angle)
                    * self.incr_angle - (3*pi/4))
            self.set_value_by_angle(angle)
    
    def pack(self, **kwargs):
        self.widget.pack(**kwargs)


class osccontroller:
    def __init__(self, parent, target):
        self.osc = target
        self.osc_octave = 4
        self.osc_note = 0
        self.osc_detune = 0
        self.osc_ampl = 1
        self.widget = tkinter.Frame(parent, bd=1, relief=RAISED, pady=3,
            padx=3)
        self.widget.pack(side=LEFT)
        self.enabled = False
        
        # individual controls
        self.w_top_frame = tkinter.Frame(self.widget, pady=5)
        self.w_ampl = dialwidget(self.w_top_frame,
            dmin=0, dmax=100, dinitial=100, text="Volume",
            dmintext='0%', dmaxtext='100%',
            callback=self.set_ampl)
        self.w_label = tkinter.Label(self.w_top_frame, padx=5,
            text="Oscillator", font="Fixed 8")
        self.w_toggle = tkinter.Button(self.w_top_frame,
            font="Fixed 9", command=self.toggle_enabled)
        self.w_ampl.pack(side=RIGHT)
        self.w_label.pack(side=RIGHT, expand=1)
        self.w_toggle.pack(side=LEFT)
        self.w_top_frame.pack(side=TOP)
        
        self.w_mid_frame = tkinter.Frame(self.widget)
        self.w_freq1 = dialwidget(self.w_mid_frame,
            dmin=0, dmax=8, dinitial=4, incr=1,
            text="Octave", callback=self.set_freq_octave)
        self.w_freq2 = dialwidget(self.w_mid_frame,
            dmin=0, dmax=11, dinitial=0, incr=1,
            text="Frequency", dmintext='C', dmaxtext='B',
            callback=self.set_freq_note)
        self.w_freq3 = dialwidget(self.w_mid_frame,
            dmin=-1, dmax=1, dinitial=0, text="Detune",
            dmintext='-1', dmaxtext='+1',
            callback=self.set_freq_det)
        self.w_freq1.pack(side=LEFT)
        self.w_freq2.pack(side=LEFT)
        self.w_freq3.pack(side=LEFT)
        self.w_mid_frame.pack(side=TOP)
        
        # initialize on/off toggle to ON
        self.toggle_enabled()
    
    
    def toggle_enabled(self):
        if self.enabled:
            self.w_toggle.config(text="OFF", bg="red")
        else:
            self.w_toggle.config(text=" ON", bg="green")
        self.enabled = not self.enabled
    
    def set_freq_octave(self, value):
        self.osc_octave = int(value+0.001)
    
    def set_freq_note(self, value):
        notes = [
            "C", "CS", "D", "DS", "E", "F", "FS", "G", "GS", "A", "AS", "B"
        ]
        self.osc_note = notes[int(value+0.001)]
    
    def set_freq_det(self, value):
        self.osc_detune = value
    
    def set_ampl(self, value):
        self.osc_ampl = value
    
    def generate(self):
        if not self.enabled:
            return
        # NOTE wtOsc doesn't have a way to set detune, and
        # amplitude might require a different implementation (TODO?)
        return self.osc.genOutput([self.osc_note, self.osc_octave])



class seqstep:
    def __init__(self, parent, step):
        self.step = step
        self.widget = tkinter.Button(parent,
            text="{:02d}".format(step), font="Fixed 9", command=self.go)
        self.widget.pack(side=LEFT)
    
    def go(self):
        global osc
        # NOTE this is very temporary!
        # It will also freeze the interface for a while when invoked
        import serial
        ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
        print("Generating...")
        print("Note: {}{}".format(osc.osc_note, osc.osc_octave))
        for t in range(0, 1000):
            out = bytes([osc.generate()])
            #print(out)
            ser.write(out)
        print("Stopping")


class seqbar:
    def __init__(self, parent, length):
        self.length = length
        self.widget = tkinter.Frame(parent)
        self.widget.pack(side=BOTTOM)
        self.steps = [seqstep(self.widget, i) for i in range(length)]


def setup():
    tk = tkinter.Tk()
    return tk


if __name__ == '__main__':
    tk = setup()
    seq = seqbar(tk, 16)
    osc = osccontroller(tk, osc.wtOsc(wave_tables=wavetables.wavetable().square()))
    tk.mainloop()
