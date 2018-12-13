from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime as dt
from datetime import timedelta as td
import pickle, time, json, datetime

class Dive:
    date = ""
    title = ""
    descr = ""
    location = ""
    address = ""
    splash = ""  # if able to get splash time, put it here

    def __str__(self):
        return '{}  {}  {}'.format(self.date, self.title, self.location)

    def __repr__(self):
        return self.__str__()

def save_cookie(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load_cookie(driver, path):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)

# Scrolls the current page to the bottom, waits pausetime, then repeats scroll. Returns after scrolltime has elapsed.
def scroll(d, pausetime, scrolltime):
    endTime = datetime.datetime.now() + td(seconds=scrolltime)
    last_height = d.execute_script("return document.body.scrollHeight")  # Get scroll height
    while datetime.datetime.now() < endTime:
        d.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll down to bottom
        time.sleep(pausetime)  # Wait to load page
        new_height = d.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print('No new data to load')  # shouldn't happen if pausetime is long enough
            break
        last_height = new_height

# Iterates through main list element in given driver, returns a list of Dive objects
def parseDives(d):
    dives = []
    # To find exact xpath, go to the ul element containing the dives in Chrome with 'inspect element' right click
    # option. Then right-click on elelment -> copy -> copy XPath.
    list = d.find_element_by_xpath('//*[@id="mupMain"]/div[4]/div[2]/div/div/div/div[2]/div/div/ul')
    for diveElem in list.find_elements_by_tag_name('li'):
        text = diveElem.text.splitlines()
        if len(text) > 1:
            try:
                i = text.index('Organizer tools')
            except ValueError:
                print('ERROR getting location:', diveElem.text)
                continue
            if i + 2 >= len(text):
                continue
            dive = Dive()
            dive.date = text[3]
            dive.title = text[4]
            dive.descr = text[7]
            dive.location = text[i + 1]
            dive.address = text[i + 2]
            print(dive)
            dives.append(dive)
    return dives

def main():
    d = webdriver.Firefox()
    d.get('https://secure.meetup.com/login')

    # Use cookie to login
    load_cookie(d, "D:\Programming\Github\Python-Projects\Dive Planner\cookies.pkl")

    # Painful process of manual login
    # data = json.loads(open('../personal_data.json').read())
    # elem = d.find_element_by_name("email")
    # elem.send_keys(data['meetup_username'])
    # elem = d.find_element_by_name("password")
    # elem.send_keys(data['meetup_password'])
    # input('Check "Im not a Robot box", then login. Enter any key to continue.')
    # save_cookie(d, "D:\Programming\Github\Python-Projects\Dive Planner\cookies.pkl")

    d.get('https://www.meetup.com/Marker-Buoy-Dive-Club/events/past')

    print('Scrolling')
    scroll(d, 4, 60)

    print('Parsing dives')
    dives = parseDives(d)

    print('Saving dive data')
# with open("dive_past_data.tsv", 'w') as f:
    #     print('Starting Parse')








if __name__ == "__main__":
    main()
