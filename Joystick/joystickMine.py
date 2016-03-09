import pygame

pygame.init()
pygame.joystick.init()

while True:
    pygame.event.pump()

    joystick_count = pygame.joystick.get_count()

    for i in range(joystick_count):  # For each joystick:
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        axes = joystick.get_numaxes()

        for i in range( axes ):
            axes = joystick.get_axis( i )
            print(axes)

    pygame.time.wait(200)
