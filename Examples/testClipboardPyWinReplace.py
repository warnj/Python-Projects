# The following piece of code replaces all newlines in the clipboard by spaces, then
# removes all double spaces and finally saves the content back to the clipboard:

import win32clipboard

win32clipboard.OpenClipboard()
c = win32clipboard.GetClipboardData()
win32clipboard.EmptyClipboard()
c = c.replace('\n', ' ')
c = c.replace('\r', ' ')
while c.find('  ') != -1:
    c = c.replace('  ', ' ')
win32clipboard.SetClipboardText(c)
win32clipboard.CloseClipboard()