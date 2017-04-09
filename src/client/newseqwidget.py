import tkinter
from tkinter.constants import *

NOTE_WIDTH = 16
NOTE_HEIGHT = 8

NOTE_NAMES = [
    "C", "CS", "D", "DS", "E", "F", "FS", "G", "GS", "A", "AS", "B"
]

def NOTE_PARITY(nidx):
    ''' Returns true for piano black keys, false for piano white keys '''
    return NOTE_NAMES[nidx % len(NOTE_NAMES)][-1] == "S"

class Sequencer:
    ''' Canvas-based Sequencer widget. '''
    def __init__(self, parent, length, height, firstnoteidx, temposource):
        # regular data
        self.parent = parent
        self.length = length
        self.height = height
        self.highnote = firstnoteidx + self.height
        self.temposource = temposource
        
        # current mouse state
        self._dragging = False
        self._reverse_dragging = False
        self._drag_start_x = None
        self._drag_start_y = None
        
        # encapsulated widget
        self.widget = tkinter.Canvas(
            parent,
            height=self.height*NOTE_HEIGHT + 1,
            width=self.length*NOTE_WIDTH + 1,
            background='gray50'
        )
        
        self.widget.bind("<Button-1>", self._mouse_down)
        self.widget.bind("<ButtonRelease-1>", self._mouse_up)
        self.widget.bind("<Motion>", self._mouse_move)
        
        # note grid
        self.notes = [
            [
                self.widget.create_rectangle(
                    1 + x * NOTE_WIDTH,
                    1 + y * NOTE_HEIGHT,
                    1 + (x+1) * NOTE_WIDTH,
                    1 + (y+1) * NOTE_HEIGHT,
                    fill=('black' if NOTE_PARITY(self._nidx(y)) else 'gray25'),
                    outline='gray50'
                ) for y in range(height)
            ] for x in range(length)
        ]
        
        # step data
        self.steps = [None for x in range(length)]
        self.step_is_continuous = [False for x in range(length)]
    
    
    def _mouse_down(self, ev):
        grid_x, grid_y = self._to_grid(ev.x, ev.y)
        
        self._dragging = True
        self._drag_start_x = ev.x
        self._drag_start_y = ev.y
        if self.steps[grid_x] == grid_y:
            self._set_deselected(grid_x, grid_y)
            self.steps[grid_x] = None
            self.step_is_continuous[grid_x] = False
            self._reverse_dragging = True
        else:
            if self.steps[grid_x] is not None:
                self._set_deselected(grid_x, self.steps[grid_x])
            self._set_selected(grid_x, grid_y)
            self.steps[grid_x] = grid_y
            self.step_is_continuous[grid_x] = False
            self._reverse_dragging = False
            
        if grid_x + 1 in range(self.length):
            if self.step_is_continuous[grid_x + 1]:
                # a continuous step is always selected
                self._set_selected(grid_x+1, self.steps[grid_x+1])
                self.step_is_continuous[grid_x + 1] = False
    
    
    def _mouse_up(self, ev):
        self._dragging = False
    
    
    def _mouse_move(self, ev):
        if self._dragging:
            grid_x, grid_y = self._to_grid(ev.x, ev.y)
            if grid_x < 0 or grid_x >= self.length:
                return
            
            start_grid_x, start_grid_y = (
                self._to_grid(self._drag_start_x, self._drag_start_y))
            if not self._reverse_dragging:
                if grid_x > start_grid_x:
                    if self.steps[grid_x] is not None:
                        self._set_deselected(grid_x, self.steps[grid_x])
                    self._set_continuous(grid_x, start_grid_y)
                    self.steps[grid_x] = start_grid_y
                    self.step_is_continuous[grid_x] = True
            else:
                if self.steps[grid_x] is not None:
                    self._set_deselected(grid_x, self.steps[grid_x])
                    self.steps[grid_x] = None
                    self.step_is_continuous[grid_x] = False
            if grid_x + 1 in range(self.length):
                if (self.step_is_continuous[grid_x + 1]
                    and self.steps[grid_x + 1] != start_grid_y):
                    # a continuous step is always selected
                    self._set_selected(grid_x+1, self.steps[grid_x+1])
                    self.step_is_continuous[grid_x + 1] = False
    
    
    def _to_grid(self, x, y):
        return (
            (x - 1) // NOTE_WIDTH,
            (y - 1) // NOTE_HEIGHT
        )
    
    
    def _set_selected(self, x, y):
        self.widget.itemconfigure(self.notes[x][y],
            fill=('gray75' if NOTE_PARITY(self._nidx(y)) else 'white'))
    
    
    def _set_deselected(self, x, y):
        self.widget.itemconfigure(self.notes[x][y],
            fill=('black' if NOTE_PARITY(self._nidx(y)) else 'gray25'))
    
    
    def _set_continuous(self, x, y):
        self.widget.itemconfigure(self.notes[x][y],
            fill=('gray50' if NOTE_PARITY(self._nidx(y)) else 'gray75'))
    
    
    def _nidx(self, y):
        ''' Converts a y-coordinate to a note number. '''
        return self.highnote - y
    
    
    def sequence(self):
        tempo = self.temposource()
        seq = []
        nlen = 0
        for i in range(self.length):
            if self.steps[i] is None:
                nlen += 1
            else:
                if nlen > 0:
                    seq.append([None, nlen])
                    nlen = 0
                if self.step_is_continuous[i]:
                    seq[-1][1] += 1 * tempo
                else:
                    nidx = self._nidx(self.steps[i])
                    note = NOTE_NAMES[nidx % len(NOTE_NAMES)]
                    octave = nidx // len(NOTE_NAMES)
                    seq.append([[note, octave], 1 * tempo])
        # allow releases to complete
        seq.append([None, 5.0])
        return seq
    
    
    def pack(self, **kwargs):
        ''' Packs the underlying widget. '''
        self.widget.pack(**kwargs)
