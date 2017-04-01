# TODO: Imports awaiting oscillator implementation.

# For graphics
import tkinter
from tkinter.constants import *


class dialwidget:
    def __init__(self, parent, dmin, dmax, dinitial, text, callback):
        self.dmin = dmin
        self.dmax = dmax
        self.text = text
        self.dragging = False
        self.value = dinitial
        self.callback = callback
        self.widget = tkinter.Canvas(parent, width=50, height=50,
            relief=FLAT
        )
        self.wd_label = self.widget.create_text(
            25, 6, justify="center", fill="white", font="Fixed 6", text=text)
        self.wd_minlabel = self.widget.create_text(
            25-15-3, 30+15, justify="right", fill="white", font="Fixed 4",
            text=str(dmin)
        )
        self.wd_maxlabel = self.widget.create_text(
            25+15+3, 30+15, justify="left", fill="white", font="Fixed 4",
            text=str(dmax)
        )
        self.wd_circle = self.widget.create_oval(
            25-15, 30-15, 25+15, 30+15, outline="white", fill="white",
            stipple="gray25")
        self.widget.bind('<Button-1>', self.mouse_down)
        self.widget.bind('<Motion>', self.mouse_handle)
        self.widget.bind('<ButtonRelease-1>', self.mouse_up)
        self.wd_indic = self.widget.create_line(25, 30-15, 25, 30-10,
            fill="white")
        self.set_value_by_angle(0)
    
    def set_value_by_angle(self, angle):
        from math import sin, cos, pi
        xr = cos(angle - (pi/2))
        yr = sin(angle - (pi/2))
        
        x1 = 25 + (15 * xr)
        y1 = 30 + (15 * yr)
        x2 = 25 + (5 * xr)
        y2 = 30 + (5 * yr)
        
        self.widget.coords(self.wd_indic, x1, y1, x2, y2)
        
        # converting (-3pi/4) <--> (3pi/4) to (MIN) <--> (MAX)
        value = ((angle * (self.dmax - self.dmin) * 4 / (3 * pi))
                + self.dmax + self.dmin) / 2
        self.value = value
        self.callback(self.value)
    
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
            self.set_value_by_angle(angle)
    
    def pack(self, **kwargs):
        self.widget.pack(**kwargs)


class osccontroller:
    def __init__(self, parent, target):
        self.osc = target
        self.widget = tkinter.Frame(parent, bd=1, relief=RAISED, pady=3,
            padx=3)
        self.widget.pack(side=LEFT)
        self.enabled = False
        
        # individual controls
        # TODO: This might change depending on oscillator
        # implementation, especially the limits on the dials
        # which are currently random guesses
        self.w_top_frame = tkinter.Frame(self.widget, pady=5)
        self.w_label = tkinter.Label(self.w_top_frame, padx=5,
            text="Oscillator", font="Fixed 8")
        self.w_toggle = tkinter.Button(self.w_top_frame,
            font="Fixed 9", command=self.toggle_enabled)
        self.w_label.pack(side=RIGHT, expand=1)
        self.w_toggle.pack(side=LEFT)
        self.w_top_frame.pack(side=TOP)
        
        self.w_bot_frame = tkinter.Frame(self.widget)
        self.w_freq = dialwidget(self.widget,
            dmin=100, dmax=200, dinitial=150, text="Frequency",
            callback=self.set_freq)
        self.w_ampl = dialwidget(self.widget,
            dmin=0, dmax=20, dinitial=10, text="Volume",
            callback=self.set_ampl)
        self.w_freq.pack(side=LEFT)
        self.w_ampl.pack(side=RIGHT)
        self.w_bot_frame.pack(side=BOTTOM)
        
        # initialize on/off toggle to ON
        self.toggle_enabled()
    
    # TODO: actually control an oscillator
    def toggle_enabled(self):
        if self.enabled:
            self.w_toggle.config(text="OFF", bg="red")
        else:
            self.w_toggle.config(text=" ON", bg="green")
        self.enabled = not self.enabled
    
    def set_freq(self, value):
        pass
    
    def set_ampl(self, value):
        pass



class seqstep:
    def __init__(self, parent, step):
        self.step = step
        self.widget = tkinter.Button(parent,
            text="{:02d}".format(step), font="Fixed 9")
        self.widget.pack(side=LEFT)


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
    osc = osccontroller(tk, None)
    tk.mainloop()
