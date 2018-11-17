__author__ = 'Alexander Gorkun'

import Tkinter as tk


class KeyButton(tk.Button):
    edit_widget = None

    symbol = None

    def __init__(self, master, edit_widget, symbol=None, cnf={}, **kw):
        tk.Button.__init__(self, master=master, cnf=cnf, **kw)
        assert isinstance(edit_widget, tk.Text)
        self.edit_widget = edit_widget
        if symbol:
            self.symbol = str(symbol)
            if not self['text']:
                self.config(text=self.symbol)
        self.config(command=self._change_text)

    def _change_text(self):
        if self.symbol:
            self.edit_widget.insert(tk.END, self.symbol)


class Backspace(KeyButton):
    def __init__(self, master, edit_widget, text='<--', cnf={}, **kw):
        KeyButton.__init__(self, master, edit_widget, text=text, cnf=cnf, **kw)

    def _change_text(self):
        txt = str(self.edit_widget.get("1.0", tk.END))[:-2]
        self.edit_widget.delete("1.0", tk.END)
        self.edit_widget.insert(tk.INSERT, txt)