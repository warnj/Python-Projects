#! /usr/bin/python

# found this online, searches google

import os 
import urllib 

# pop-up box that you type input to:
google = os.popen('zenity --entry --text="Enter what you want to google: " --title="google.py"').read() 

# prompts for input in terminal:
# google = raw_input('Enter search terms: ')

# uses first command-line-argument as search term
#import sys
#google = sys.argv[1]

google = urllib.quote(google) 
os.system('google-chrome http://www.google.com/search?q=%s' % (google))  
