import pygame

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() != 1:
    print "Joystick not connected"
else:
    print "Joystick connected"
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

while True:
    for event in pygame.event.get(): # User did something
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

        axes = joystick.get_numaxes()
        # axis 0 = aileron   -1.0 = left, 0.0 = neutral, 1.0 = right
        # axis 1 = elevator   -1.0 = forward, 0.0 = neutral, 1.0 = back
        # axis 2 = throttle   -1.0 = full, 0.0 = half, 1.0 = idle
        # axis 3 = rudder   -1.0 = left, 0.0 = neutral, 1.0 = right
        for i in range( axes ):
            axis = joystick.get_axis( i )
            print "Axis %d value: %f" % (i, axis)

'''
        buttons = joystick.get_numbuttons()
        for i in range( buttons ):
            button = joystick.get_button( i )

        hats = joystick.get_numhats()
        for i in range( hats ):
            hat = joystick.get_hat( i )
        '''

pygame.quit ()
