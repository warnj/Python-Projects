import ctypes
import time

# Define necessary structures
class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort), ("wRightMotorSpeed", ctypes.c_ushort)]

xinput = ctypes.windll.xinput1_1  # Load Xinput.dll

# Set up function argument types and return type
XInputSetState = xinput.XInputSetState
XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUT_VIBRATION)]
XInputSetState.restype = ctypes.c_uint

# sets the controller vibration speed to left_motor (0.0-1.0) and right_motor (0.0-1.0)
def set_vibration(controller, left_motor, right_motor):
    vibration = XINPUT_VIBRATION(int(left_motor * 65535), int(right_motor * 65535))
    XInputSetState(controller, ctypes.byref(vibration))

# ... and use it like so
set_vibration(0, 0.5, 0.0)
time.sleep(1)
set_vibration(0, 0, 0)