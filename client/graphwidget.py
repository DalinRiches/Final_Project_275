import tkinter
from tkinter.constants import *

# for bitmap generation
import imgutil


# System to generate unique ids: just returns the
# next sequential value wheneve it's called
_uid = 0
def g_next_uid():
    global _uid
    u = _uid
    _uid += 1
    return str(u)


class GraphScreen:
    ''' A canvas-derived widget for displaying a function
    as a bitmap. Works for any function of y in x, rendering
    to a Canvas widget.

    Parameters:
        parent: (Widget) tk-style parent widget.
        width: (int) width in pixels of the canvas; also the
            domain of x in which the function will be drawn.
            (As a region, (0, width].) To set different domains,
            scale the bound function mathematically.
        height: (int) height in pixels of the canvas; also the
            maximum range of y which will be drawn. (As a region,
            (o, height].) To set different drawing ranges, scale
            the bound function mathematically.
        fx: (function): function that takes an integer and returns
            an integer. This is the function that will be drawn
            to the graph. '''

    def __init__(self, parent, width, height, fx):
        ''' Initializer for GraphScreen - sets up a canvas,
        assigns a unique image id, and initially renders. '''

        # regular data
        self.fx = fx
        self.width = width
        self.height = height
        self.parent = parent
        self.image = None

        # unique id
        self.uid = g_next_uid()

        # function bitmap
        self.bits = bytearray(width*height//8)

        # encapsulated widget
        self.widget = tkinter.Canvas(
            parent,
            width=width,
            height=height,
            background="yellow"
        )

        # initial redraw
        self.redraw()


    def redraw(self):
        ''' Draws a representation of the function fx
        to the encapsulated canvas. '''

        # save previous y for interpolation
        yprev = None

        for x in range(self.width):
            y = self.fx(x)
            self._write_column(x, y, yprev)
            yprev = y
        self._make_bitmap()


    def _make_bitmap(self):
        ''' Turns the stored bits created by _write_column etc
        into a bitmap that Tkinter can parse. '''

        # get bitmap data
        self.bitmap = imgutil.tobitmap(self.bits, self.width, self.height)

        # make or modify Tkinter image object
        if self.image is None:
            self.image = tkinter.BitmapImage(
                name='graphimg-'+self.uid,
                data=self.bitmap,
                foreground='white',
                background='black'
            )
        else:
            self.image.configure(data=self.bitmap)

        # draw to canvas
        self.imageobj = self.widget.create_image(
            1, 1,
            anchor=NW,
            image=self.image
        )


    def _write_column(self, x, y, yprev=None):
        ''' Sets pixel y in column x on and the rest of the pixels
        in the column off. If yprev is specified, interpolates
        from the given value by filling in the pixels in column x
        between the two y-values, giving a continuous graph (given
        yprev is actually the previous y). '''

        for yi in range(self.height):
            if (yi == y
                or (yprev is not None and y < yi < yprev)
                or (yprev is not None and yprev < yi < y)):
                    self._write_bit(x, yi, True)
            else:
                self._write_bit(x, yi, False)


    def _write_bit(self, x, y, parity):
        ''' Writes a single bit on or off to the bitmap. '''

        bitidx = (self.height - 1 - y) * self.width + x
        byteidx = bitidx // 8
        bytemask = 0b1 << (( 7 - bitidx) % 8)

        if parity == True:
            self.bits[byteidx] |= bytemask
        else:
            self.bits[byteidx] &= (~bytemask)


    def pack(self, **kwargs):
        ''' Packs the underlying widget. '''
        self.widget.pack(**kwargs)
