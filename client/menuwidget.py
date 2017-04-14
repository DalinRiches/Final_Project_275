import tkinter
from tkinter.constants import *

class _MenuItem:
    ''' Internal class representing a single item of a Menu. Creates
    a Button widget that calls the callback function when pressed.

    Parameters:
        parent: (Widget) tk-style parent widget. Should be a Menu
            window in regular usage.
        label: (str) text to show on the button
        callback: (function) will be called when the button is pressed,
            passing the button's label.
    '''

    def __init__(self, parent, label, callback):
        ''' Initializer for _MenuItem. Creates a button. '''

        # regular data
        self.label = label
        self.callback = callback

        # encapsulated widget
        self.widget = tkinter.Button(
            parent,
            bg="gray25",
            text=label,
            font="Fixed 9",
            command=self._select
        )


    def _select(self):
        ''' Called when the button is pressed. Invokes the callback. '''
        self.callback(self.label)


    def pack(self, **kwargs):
        ''' Packs the underlying widget. '''
        self.widget.pack(**kwargs)


class Menu:
    ''' This class creates a button which opens a menu when clicked.
    It's basically a drop-down menu without the drop-down part.

    Parameters:
        parent: (Widget) tk-style parent widget
        title: (str) title of the menu, will appear in the menu window
            title bar or equivalent (it's passed as the title parameter
            of the new window)
        initial: (str) initial value to show on the button (doesn't
            actually need to be a valid menu choice)
        callback: (function) will be called whenever a new option is
            selected, passing the value corresponding to the option.
        choices: (list of tuples) each tuple represents a menu option,
            in order in the list. The first element of each tuple will
            be the text displayed on the button; the second element
            will be the string passed to the callback when the button
            is pressed.
    '''

    def __init__(self, parent, title, initial, callback, choices):
        ''' Initializer for Menu. Creates the button widget; the
        actual menu is instantiated when clicked (see Menu._invoke). '''

        # regular data
        self.parent = parent
        self.title = title
        self.label = initial
        self.callback = callback

        # toggles when the menu is opened
        self._menu_is_open = False

        # create choices dictionary
        self.set_choices(choices)

        # encapsulated widget
        self.widget = tkinter.Button(
            parent,
            bg="gray25",
            text=self.label,
            font="Fixed 9",
            command=self._invoke
        )


    def _select_item(self, item):
        ''' Called when a menu button is pressed. Closes the menu
        window and invokes the callback with the value corresponding
        to the item that was selected. The label on the menu-open
        button will be set to the item that was selected. '''
        self.w_menubox.destroy()
        self._menu_is_open = False
        if item is not None:
            self.set_label(item)
            self.callback(self._choices_dict[item])


    def set_choices(self, choices):
        ''' Sets the menu choices based on the input list of tuples.
        (See Menu.__init__ for format.) This should be called rather
        than setting self.choices directly in order to update the
        dictionary mapping. '''
        self.choices = choices
        self._choices_dict = {item[0] : item[1] for item in choices}


    def _window_close(self, ev):
        ''' Called when the menu window is closed without selecting
        anything. Just updates the state. '''
        self._menu_is_open = False


    def _invoke(self):
        ''' Called when the menu is opened. Creates a new window to
        hold the menu buttons. If the menu is already open, closes
        it instead by selecting None. (This will not invoke the
        callback.) '''

        # close menu if it is open
        if self._menu_is_open:
            self._select_item(None)
            return

        # don't show an empty menu
        if len(self.choices) == 0:
            return

        # create menu window
        self._menu_is_open = True
        self.w_menubox = tkinter.Tk()
        self.w_menubox.title(self.title)

        # bind closing the menu window
        self.w_menubox.bind('<Destroy>', self._window_close)

        # create menu options in order
        for item in self.choices:
            w_item = _MenuItem(
                parent=self.w_menubox,
                label=item[0],
                callback=self._select_item
            )
            w_item.pack(side=LEFT)


    def set_label(self, label):
        ''' Simply updates the label on the menu-open button. '''
        self.label = label
        self.widget.configure(text=label)


    def pack(self, **kwargs):
        ''' Packs the underlying widget. '''
        self.widget.pack(**kwargs)
