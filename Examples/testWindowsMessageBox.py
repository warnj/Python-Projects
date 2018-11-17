import ctypes

msgbox = ctypes.windll.user32.MessageBoxA
ret = msgbox(None, 'Press OK to end the demo.', 'Deviare Python Demo', 0)
print ret