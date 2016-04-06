#prints the HTML of the given webpage

import urllib


thisurl = "https://www.geocaching.com/login/"

handle = urllib.urlopen(thisurl)

html_gunk =  handle.read()

print html_gunk



