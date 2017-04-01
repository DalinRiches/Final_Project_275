# TODO: Imports awaiting oscillator implementation.

# For graphics
import tkinter
from tkinter.constants import *


class dialwidget:
    def __init__(self, parent, dmin, dmax, text):
        self.dmin = dmin
        self.dmax = dmax
        self.text = text
        self.widget = tkinter.Canvas(parent, width=50, height=50)
        self.wd_label = self.widget.create_text(
            25, 6, justify="center", fill="white", font="Fixed 6", text=text)
        self.wd_circle = self.widget.create_oval(
            25-15, 30-15, 25+15, 30+15, outline="white", fill="white",
            stipple="gray25")
        self.wd_indic = self.widget.create_line(25, 30-15, 25, 30-10,
            fill="white")
        
    
    def pack(self, **kwargs):
        self.widget.pack(**kwargs)


class osccontroller:
    def __init__(self, parent, target):
        self.target = target
        self.widget = tkinter.Frame(parent, bd=1, relief=RAISED, pady=3,
            padx=3)
        self.widget.pack(side=LEFT)
        
        # individual controls
        # TODO: This might change depending on oscillator
        # implementation, especially the limits on the dials
        # which are currently random guesses
        self.w_top_frame = tkinter.Frame(self.widget, pady=5)
        self.w_label = tkinter.Label(self.w_top_frame, padx=5,
            text="Oscillator", font="Fixed 8")
        self.w_toggle = tkinter.Button(self.w_top_frame, text="ON",
            font="Fixed 9", bg="green")
        self.w_label.pack(side=RIGHT, expand=1)
        self.w_toggle.pack(side=LEFT)
        self.w_top_frame.pack(side=TOP)
        
        self.w_bot_frame = tkinter.Frame(self.widget)
        self.w_freq = dialwidget(self.widget,
            dmin=100, dmax=200, text="Frequency")
        self.w_ampl = dialwidget(self.widget,
            dmin=0, dmax=20, text="Volume")
        self.w_freq.pack(side=LEFT)
        self.w_ampl.pack(side=RIGHT)
        self.w_bot_frame.pack(side=BOTTOM)
        



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
