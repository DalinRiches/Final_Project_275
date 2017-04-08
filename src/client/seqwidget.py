import tkinter
from tkinter.constants import *

_note_names = [
    "C", "CS", "D", "DS", "E", "F", "FS", "G", "GS", "A", "AS", "B"
]

def _note_parity(nidx):
    return _note_names[nidx % len(_note_names)][-1] != "S"

class _SeqNote:
    def __init__(self, seq_parent, idx):
        self.idx = idx
        self.seq_parent = seq_parent
        self.widget = tkinter.Frame(
            seq_parent.widget,
            bd=1,
            relief=RAISED,
            width=16,
            height=8
        )
        self.widget.bind('<Button-1>', self._mouse_down)
        self.widget.bind('<Motion>', self._mouse_move)
        self.widget.bind('<ButtonRelease-1>', self._mouse_up)
        
        self.widget.pack(side=TOP)
        
        self.deselect()
        self.dragging = False
    
    
    def _mouse_down(self, ev):
        if self.seq_parent.activeidx == self.idx:
            self.seq_parent._set_selected(None)
        else:
            self.seq_parent._set_selected(self.idx)
            self.dragging = True
    
    # TODO: long notes. might require rewriting entire
    # Sequence class as a canvas-based widget.
    def _mouse_move(self, ev):
        if self.dragging:
            pass
    
    def _mouse_up(self, ev):
        self.dragging = False
    
    def select(self):
        if _note_parity(self.idx):
            self.widget.config(bg='white')
        else:
            self.widget.config(bg='gray75')
    
    def deselect(self):
        if _note_parity(self.idx):
            self.widget.config(bg='gray25')
        else:
            self.widget.config(bg='black')
    

class _SeqStep:
    def __init__(self, seq_parent, height):
        self.widget = tkinter.Frame(
            seq_parent.widget,
            bd=0
        )
        
        self.notes = [_SeqNote(self, i) for i in range(height)]
        self.activeidx = None
        
        self.widget.pack(side=LEFT)
    
    
    def _set_selected(self, idx):
        if idx != self.activeidx and self.activeidx is not None:
            self.notes[self.activeidx].deselect()
        if idx is not None:
            self.notes[idx].select()
        self.activeidx = idx
    
    def get_note(self):
        if self.activeidx is None:
            return None
        
        octave = (self.activeidx // 12) + 3
        note = _note_names[self.activeidx % 12]
        return [[note, octave], 0.5]


class Sequencer:
    def __init__(self, parent, length, height):
        self.widget = tkinter.Frame(
            parent,
            bd=3,
            relief=RIDGE
        )
        
        self.steps = [_SeqStep(self, height) for i in range(length)]
    
    def pack(self, **kwargs):
        self.widget.pack(**kwargs)
    
    def sequence(self):
        seq = []
        for step in self.steps:
            note = step.get_note()
            if note is not None:
                seq.append(note)
        return seq
