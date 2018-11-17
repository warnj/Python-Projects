import time, sys, select, msvcrt

'''
for i in range(0, 10):
    stuff = raw_input("Give me a string: ")
    print "\ryou gave me: " + stuff

'''

'''
import time
from threading import Thread

answer = None

def check():
    time.sleep(2)
    if answer != None:
        return
    print "Too Slow"

Thread(target = check).start()

answer = raw_input("You have 2s to input something: ")
'''


import time

def sleeper():
    while True:
        # Get user input
        num = raw_input('How long to wait: ')

        # Try to convert it to a float
        try:
            num = float(num)
        except ValueError:
            print('Please enter in a number.\n')
            continue

        # Run our time.sleep() command,
        # and show the before and after time
        print('Before: %s' % time.ctime())
        time.sleep(num)
        print('After: %s\n' % time.ctime())


try:
    sleeper()
except KeyboardInterrupt:
    print('\n\nKeyboard exception received. Exiting.')
    exit()