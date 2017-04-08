import tkinter
from tkinter.constants import *


class Dial:
    ''' A visual dial for entering numerical values. Can be rotated
    by clicking and dragging and reset by double-clicking.
    
    Parameters:
        parent: (Widget) tk-style parent widget.
        dmin: (float) minimum value the dial can be set to.
        dmax: (float) maximum value the dial can be set to.
        dinitial: (float) default value for the dial. It will be
            instantiated with this value and will return to it
            when double-clicked.
        label: (str) label for the dial.
        callback: (function) function to be called when the dial
            setting is changed. Will be passed the new value, and
            the label of the dial if it is a three-argument
            function.
        dmintext: (str) (optional) label for the minimum value.
            If unset defaults to the string representation of
            the actual minimum value.
        dmaxtext: (str) (optional) label for the maximum value.
            If unset defaults to the string representation of
            the actual maximum value.
        dincrement: (float) (optional) step increment. If set,
            the dial will snap to the closest multiple of this
            value when turned. Note that floating point error
            may cause multiples to be somewhat inexact, which
            may be problematic in certain situations.
    '''
    def __init__(self, parent, dmin, dmax, dinitial, label, callback,
                 dmintext=None, dmaxtext=None, dincrement=None):
        # Basic parameters: minimum, maximum, initial values
        self.dmin = dmin
        self.dmax = dmax
        self.dinitial = dinitial
        
        # Text: main label, min value text, max value text
        self.label = label
        
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
        if dincrement is not None:
            from math import pi
            self.incr = dincrement
            self.incr_angle = (3*pi/2) / ((dmax - dmin)/dincrement)
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
            25, 6, justify="center", fill="white", font="Fixed 6", text=label)
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
            stipple="gray25"
        )
        # Current value box
        self.wd_valbox = self.widget.create_rectangle(
            25-9, 30+15+3-5, 25+8, 30+15+3+3, outline="white", fill="black"
        )
        # Current value label
        self.wd_vallabel = self.widget.create_text(
            25, 30+15+3, justify="center", fill="white", font="Fixed 4",
            text="###"
        )
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
        self._callback(self.value, self.label)
    
    
    def _callback(self, value, label):
        argc = self.callback.__code__.co_argcount # ...
        if argc == 3:
            self.callback(value, label)
        elif argc == 2:
            self.callback(value)
        else:
            raise RuntimeError("Invalid callback signature in dial")
    
    
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
