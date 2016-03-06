# prints what is in the clipboard (think copy/paste)

from Tkinter import Tk

result=Tk().clipboard_get()
print result