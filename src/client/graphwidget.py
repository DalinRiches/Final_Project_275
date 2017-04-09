import tkinter
from tkinter.constants import *

import imgutil


# System to generate unique ids
_uid = 0
def g_next_uid():
    global _uid
    u = _uid
    _uid += 1
    return str(u)


class GraphScreen:
    ''' A canvas-derived widget for displaying a function
    as a bitmap. '''
    
    def __init__(self, parent, width, height, fx):
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
        yprev = None
        for x in range(self.width):
            y = self.fx(x)
            self._write_column(x, y, yprev)
            yprev = y
        self._make_bitmap()
    
    
    def _make_bitmap(self):
        self.bitmap = imgutil.tobitmap(self.bits, self.width, self.height)
        if self.image is None:
            self.image = tkinter.BitmapImage(
                name='graphimg-'+self.uid,
                data=self.bitmap,
                foreground='white',
                background='black'
            )
        else:
            self.image.configure(data=self.bitmap)
        #print(self.image)
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
