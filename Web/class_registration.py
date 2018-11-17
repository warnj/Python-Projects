from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import firefox
from selenium.webdriver.common.keys import Keys
import time, datetime, sys

# this program will register for all the given sln numbers at exactly 6am

# need the versions of geckodriver that corresponds to current Firefox version
# in the path - can try updating them both if issues

# TODO: shouldn't need to manually specify if the next 6am is going to occur today or tomorrow.
OPTION = "DEBUG"
# OPTION = "TODAY"
# OPTION = "TOMORROW"


def exit():
    raw_input('Press any key to exit')
    # TODO: close the driver here
    sys.exit(0)


data = json.loads(open('../personal_data.json').read())
now = datetime.datetime.now()
print("Current time: ", now)

if OPTION == "DEBUG":
    # DEBUG ONLY:
    target_time = now + datetime.timedelta(seconds=20)  # register in 20sec
    print("Registration system test at: ", target_time)
    sec_to_sleep = (target_time - now).total_seconds() - 17  # for debug start Firefox 17sec before registering
elif OPTION == "TODAY":
    # REAL REGISTRATION TODAY 6am:
    target_time = now.replace(hour=6, minute=0, second=0, microsecond=0)
    print("Registering today at: ", target_time)
    sec_to_sleep = (target_time - now).total_seconds() - 60  # start continually checking for 6am 60secs before 6am
else:
    # REAL REGISTRATION TOMORROW 6am:
    tom = now + datetime.timedelta(days=1)  # move one day ahead
    target_time = tom.replace(hour=6, minute=0, second=0, microsecond=0)  # set exact time to 6am
    print("Registering tomorrow at: ", target_time)
    sec_to_sleep = (target_time - now).total_seconds() - 60  # start continually checking for 6am 60secs before 6am

print("Waiting %d seconds before opening browser" % sec_to_sleep)
time.sleep(sec_to_sleep)  # sleep overnight

now = datetime.datetime.now()
print("Launching browser, registering in %s seconds" % (target_time - now).total_seconds())

binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary)

driver.get("https://sdb.admin.uw.edu/students/uwnetid/register.asp")
# assert "NetID" in driver.title
# print driver.title
driver.maximize_window()
time.sleep(1)
elem = driver.find_element_by_name("user")
elem.send_keys(data['uw_username'])
elem = driver.find_element_by_name("pass")
elem.send_keys(data['uw_password'])
elem.send_keys(Keys.RETURN)
# assert "Registration" in driver.title
# print driver.title


while True:
    now = datetime.datetime.now()
    if now > target_time:
        print('Starting registration')
        break

# refresh at exactly 6am
# IMPORTANT: the number after "sln" corresponds to how many classes/sections/labs you are currently 
# registered for, so these should probably be numbered sln1 - sln8
driver.refresh()
time.sleep(1)

# this worked really fast on 11/8
raw_input("PRESS ANY KEY AND ENTER WHEN THE PAGE IS DONE LOADING!!!!!!!!!!!!!!!!")

elem = driver.find_element_by_name("sln1")
elem.send_keys("19658")  # SLN #1
elem = driver.find_element_by_name("sln2")
elem.send_keys("19659")  # SLN #2
# elem = driver.find_element_by_name("sln3")
# elem.send_keys("12827") #SLN #3
# elem = driver.find_element_by_name("sln4")
# elem.send_keys("12828") #SLN #4
# elem = driver.find_element_by_name("sln5")
# elem.send_keys("13081") #SLN #5
# elem = driver.find_element_by_name("sln6")
# elem.send_keys("13050") #SLN #6
# elem = driver.find_element_by_name("sln7")
# elem.send_keys("13052") #SLN #6
# elem = driver.find_element_by_name("sln8")
# elem.send_keys("13034") #SLN #6
# elem = driver.find_element_by_name("sln9")
# elem.send_keys("13038") #SLN #6


# elem.send_keys(Keys.RETURN)
'''


try: # look for the failure image on the page
    elem = driver.find_element_by_xpath("//img[contains(@src,'/sdb_library/images/warning.gif')]")
    print "registration failed"
    # return to blank registration page
    driver.get("https://sdb.admin.uw.edu/students/uwnetid/register.asp")

except:
    print "registration succeeded in 1 try"
    driver.close()
    exit()
'''

'''

# 2nd choice of classes:

elem = driver.find_element_by_name("sln1")
elem.send_keys("12345") #SLN #1
elem = driver.find_element_by_name("sln2")
elem.send_keys("67891") #SLN #2
elem = driver.find_element_by_name("sln3")
elem.send_keys("23456") #SLN #3
elem = driver.find_element_by_name("sln4")
elem.send_keys("12345") #SLN #4
elem = driver.find_element_by_name("sln5")
elem.send_keys("67891") #SLN #5
elem = driver.find_element_by_name("sln6")
elem.send_keys("23456") #SLN #6

elem.send_keys(Keys.RETURN)




try: # look for the failure image on the page
    elem = driver.find_element_by_xpath("//img[contains(@src,'/sdb_library/images/warning.gif')]")
    print "registration failed"
    # return to blank registration page
    driver.get("https://sdb.admin.uw.edu/students/uwnetid/register.asp")

except:
    print "registration succeeded in 2 tries"
    driver.close()
	exit()






# 3rd choice of classes:

elem = driver.find_element_by_name("sln1")
elem.send_keys("12345") #SLN #1
elem = driver.find_element_by_name("sln2")
elem.send_keys("67891") #SLN #2
elem = driver.find_element_by_name("sln3")
elem.send_keys("23456") #SLN #3
elem = driver.find_element_by_name("sln4")
elem.send_keys("12345") #SLN #4
elem = driver.find_element_by_name("sln5")
elem.send_keys("67891") #SLN #5
elem = driver.find_element_by_name("sln6")
elem.send_keys("23456") #SLN #6

elem.send_keys(Keys.RETURN)


try: # look for the failure image on the page
    elem = driver.find_element_by_xpath("//img[contains(@src,'/sdb_library/images/warning.gif')]")
    print "registration failed"
    # return to blank registration page
    driver.get("https://sdb.admin.uw.edu/students/uwnetid/register.asp")

except:
    print "registration succeeded in 3 tries"
    driver.close()
	exit()







# 4th choice of classes:

elem = driver.find_element_by_name("sln1")
elem.send_keys("12345") #SLN #1
elem = driver.find_element_by_name("sln2")
elem.send_keys("67891") #SLN #2
elem = driver.find_element_by_name("sln3")
elem.send_keys("23456") #SLN #3
elem = driver.find_element_by_name("sln4")
elem.send_keys("12345") #SLN #4
elem = driver.find_element_by_name("sln5")
elem.send_keys("67891") #SLN #5
elem = driver.find_element_by_name("sln6")
elem.send_keys("23456") #SLN #6

elem.send_keys(Keys.RETURN)


try: # look for the failure image on the page
    elem = driver.find_element_by_xpath("//img[contains(@src,'/sdb_library/images/warning.gif')]")
    print "registration failed"
    # return to blank registration page
    driver.get("https://sdb.admin.uw.edu/students/uwnetid/register.asp")

except:
    print "registration succeeded in 4 tries"
    


driver.close()
exit()


'''
