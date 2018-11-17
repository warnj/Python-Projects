import ctypes, pygame, time

# Define necessary structures
class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort), ("wRightMotorSpeed", ctypes.c_ushort)]

# sets the controller vibration speed to left_motor (0.0-1.0) and right_motor (0.0-1.0)
def set_vibration(controller, left_motor, right_motor):
    vibration = XINPUT_VIBRATION(int(left_motor * 65535), int(right_motor * 65535))
    XInputSetState(controller, ctypes.byref(vibration))

xinput = ctypes.windll.xinput1_1  # Load Xinput.dll

# Set up function argument types and return type
XInputSetState = xinput.XInputSetState
XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUT_VIBRATION)]
XInputSetState.restype = ctypes.c_uint

pygame.init()
done = False
pygame.joystick.init()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        name = joystick.get_name()
        axes = joystick.get_numaxes()
        axis = joystick.get_axis(2)
        left = 0
        right = 0
        if(axis > 0.001):
            left = axis
            right = 0
        elif(axis < -0.001):
            right = -axis
            left = 0
        set_vibration(0, left, right)

    time.sleep(.03)
    done = joystick.get_button(2)  # press X button on xbox controller to quit

pygame.quit()
