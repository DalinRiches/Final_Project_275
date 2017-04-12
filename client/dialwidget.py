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
        valformat: (str) (optional) a format string that will
            be used to convert values to text; used for the
            current, min, and max value labels.
        valcallback: (function) (optional) a function that takes
            a float and returns a string, used to format current,
            min, and max value labels. Overrides valformat.
        dmintext: (str) (optional) label for the minimum value.
            If unset defaults to the string representation of
            the actual minimum value as given by valformat.
        dmaxtext: (str) (optional) label for the maximum value.
            If unset defaults to the string representation of
            the actual maximum value as given by valformat.
        dincrement: (float) (optional) step increment. If set,
            the dial will snap to the closest multiple of this
            value when turned. Note that floating point error
            may cause multiples to be somewhat inexact, which
            may be problematic in certain situations.
    '''
    def __init__(self, parent, dmin, dmax, dinitial, label, callback,
                 valformat=None, valcallback=None,
                 dmintext=None, dmaxtext=None, dincrement=None):
        ''' Initializer for Dial. Creates a Canvas widget which will
        display the dial body and labels, and binds mouse events to
        allow the dial to be interacted with. For parameters see
        class documentation. '''

        # Basic parameters: minimum, maximum, initial values and formatters
        self.dmin = dmin
        self.dmax = dmax
        self.dinitial = dinitial
        self.valformat = valformat
        self.valcallback = valcallback

        # Text: main label, min value text, max value text
        self.label = label

        # If no min/max labels specified, use formatted values
        if dmintext is None:
            self.dmintext = self._format(self.dmin)
        else:
            self.dmintext = dmintext
        if dmaxtext is None:
            self.dmaxtext = self._format(self.dmax)
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

        # Create encapsulated widget
        self.widget = tkinter.Canvas(
            parent,
            width=50,
            height=50,
            relief=FLAT
        )

        # Subitems of widget:
        # Main text label
        self.wd_label = self.widget.create_text(
            25, 6,
            justify="center",
            fill="white",
            font="Fixed 6",
            text=label
        )
        # Min value label
        self.wd_minlabel = self.widget.create_text(
            25-15-3, 30+15,
            justify="right",
            fill="white",
            font="Fixed 4",
            text=self.dmintext
        )
        # Max value label
        self.wd_maxlabel = self.widget.create_text(
            25+15+3, 30+15,
            justify="left",
            fill="white",
            font="Fixed 4",
            text=self.dmaxtext
        )
        # Dial body
        self.wd_circle = self.widget.create_oval(
            25-15, 30-15,
            25+15, 30+15,
            outline="white",
            fill="white",
            stipple="gray25"
        )
        # Current value box
        self.wd_valbox = self.widget.create_rectangle(
            25-9, 30+15+3-5,
            25+8, 30+15+3+3,
            outline="white",
            fill="black"
        )
        # Current value label
        self.wd_vallabel = self.widget.create_text(
            25, 30+15+3,
            justify="center",
            fill="white",
            font="Fixed 4",
            text="###"
        )
        # Dial body events: click/move/release to change,
        # double-click to reset
        self.widget.bind('<Button-1>', self.mouse_down)
        self.widget.bind('<Double-Button-1>', self.mouse_dbl)
        self.widget.bind('<Motion>', self.mouse_handle)
        self.widget.bind('<ButtonRelease-1>', self.mouse_up)

        # Dial pointer
        self.wd_indic = self.widget.create_line(
            25, 30-15,
            25, 30-10,
            fill="white"
        )

        # Initialize pointer location and callback
        self.set_value_by_angle(self.val_to_angle(dinitial))


    def angle_to_val(self, angle):
        ''' Converts an angle in radians to a dial value. '''

        # converting (-3pi/4) <--> (3pi/4) to (MIN) <--> (MAX)
        from math import pi

        value = ((angle * (self.dmax - self.dmin) * 4 / (3 * pi))
                + self.dmax + self.dmin) / 2
        return value


    def val_to_angle(self, value):
        ''' Converts a dial value to an angle in radians. '''

        # converting (MIN) <--> (MAX) to (-3pi/4) <--> (3pi/4)
        from math import pi

        angle = ((3 * pi * (2 * value - (self.dmax + self.dmin)))
                / (4 * (self.dmax - self.dmin)))
        return angle


    def set_value_by_angle(self, angle):
        ''' Sets the dial to point to a specific angle and updates
        the value accordingly. The callback function will be invoked
        and the current-value label will be updated. '''

        from math import sin, cos, pi

        # coordinates of the pointer from 0, 0
        xr = cos(angle - (pi/2))
        yr = sin(angle - (pi/2))

        # coordinates transformed to dial-body space
        x1 = 25 + (15 * xr)
        y1 = 30 + (15 * yr)
        x2 = 25 + (5 * xr)
        y2 = 30 + (5 * yr)

        # move dial pointer
        self.widget.coords(self.wd_indic, x1, y1, x2, y2)

        # update value
        self.value = self.angle_to_val(angle)

        # update label and invoke callback
        self.widget.itemconfigure(
            self.wd_vallabel,
            text=self._format(self.value)
        )
        self._callback(self.value, self.label)


    def _callback(self, value, label):
        ''' Invokes the callback function. If the function has
        two arguments it will be passed (self, value); if it has
        three it will be passed (self, value, label). '''

        # this retrieves the number of arguments in the callback signature
        argc = self.callback.__code__.co_argcount

        if argc == 3:
            self.callback(value, label)
        elif argc == 2:
            self.callback(value)
        else:
            raise RuntimeError("Invalid callback signature in dial")


    def _format(self, value):
        ''' Converts a value to a string based on the dial's
        format callback, if it exists, else the dials format string;
        if neither exists uses a default format string. '''

        if self.valcallback is not None:
            return self.valcallback(value)
        elif self.valformat is not None:
            return self.valformat.format(value)
        else:
            return "{:.1f}".format(value)


    def mouse_dbl(self, ev):
        ''' Double-click handler: resets the dial to its initial value '''
        self.set_value_by_angle(self.val_to_angle(self.dinitial))


    def mouse_down(self, ev):
        ''' Click handler: sets mouse state. Nothing interesting
        happens until the mouse is moved. '''
        self.dragging = True


    def mouse_up(self, ev):
        ''' Release handler: sets mouse state. '''
        self.dragging = False


    def mouse_handle(self, ev):
        ''' Move handler: if dragging, rotate the dial to point
        towards the cursor. '''

        if self.dragging:
            from math import atan2, pi

            # angle between the dial center (30, 25) and the cursor,
            # transformed so that 0 is vertically upwards.
            angle = atan2(ev.y - 30, ev.x - 25) + (pi/2)
            if angle > pi:
                angle -= 2*pi

            # limit angle to the minimum and maximum
            angle = min(3*pi/4, max(angle, -3*pi/4))

            # apply increment by rounding to nearest multiple
            if self.incr_angle is not None:
                angle = (
                    round(
                        (angle + (3*pi/4))
                        / self.incr_angle
                    ) * self.incr_angle
                    - (3*pi/4)
                )

            # update value and callback etc.
            self.set_value_by_angle(angle)


    def pack(self, **kwargs):
        ''' Packs the underlying widget. '''
        self.widget.pack(**kwargs)
