import tkinter
from tkinter.constants import *

class _MenuItem:
    def __init__(self, parent, label, callback):
        self.label = label
        self.callback = callback
        
        self.widget = tkinter.Button(
            parent,
            bg="gray25",
            text=label,
            font="Fixed 9",
            command=self._select
        )
    
    
    def _select(self):
        self.callback(self.label)
    
    def pack(self, **kwargs):
        self.widget.pack(**kwargs)
    

class Menu:
    def __init__(self, parent, label, callback, choices):
        self.parent = parent
        self.label = label
        self.choices = choices
        self.callback = callback
        self._menu_is_open = False
        
        self.widget = tkinter.Button(
            parent,
            bg="gray25",
            text=label,
            font="Fixed 9",
            command=self._invoke
        )
    
    
    def _select_item(self, item):
        print("selected {}".format(item))
        self.w_menubox.destroy()
        self._menu_is_open = False
        if item is not None:
            self.set_label(item)
            self.callback(self.choices[item])
    
    
    def _invoke(self):
        if self._menu_is_open:
            self._select_item(None)
            return
        
        if len(self.choices) == 0:
            return
        
        self._menu_is_open = True
        self.w_menubox = tkinter.Tk()
        self.w_menubox.title(self.label)
        
        for item in self.choices.keys():
            w_item = _MenuItem(
                parent=self.w_menubox,
                label=item,
                callback=self._select_item
            )
            w_item.pack(side=LEFT)
    
    
    def set_label(self, label):
        self.label = label
        self.widget.configure(text=label)
    
    
    def pack(self, **kwargs):
        self.widget.pack(**kwargs)
