from dive_plan import Slack
from dive_plan import getSlacks
from dive_plan import getEntryTimes
from selenium import webdriver
from datetime import datetime as dt
from datetime import timedelta as td
import pickle, time, json, datetime, os, csv

MEETUP_TIME_FORMAT = '%a, %b %d, %Y, %I:%M %p'
SITE_MAP = {  # dive site -> tokens that the listing must contain
    'Day Island Wall': ['day island'],
    'Skyline Wall': ['skyline'],
    'Keystone Jetty': ['keystone'],
    'Deception Pass': ['deception pass'],
    'Fox Island Bridge': ['fox island bridge'],
    'Fox Island East Wall': ['fox island', 'east'],
    'Fox Island West Wall': ['fox island', 'west'],
    'Sunrise Beach': ['sunrise', 'beach'],
    'Three Tree North': ['three tree'],
    'Alki Pipeline': ['alki', 'pipeline'],  # this is effectively the same as junkyard
    'Alki Junkyard': ['alki', 'junk', 'yard'],
    'Saltwater State Park': ['salt', 'water', 'state', 'park'],
    'Edmonds Underwater Park': ['edmonds'],
    'Mukilteo': ['mukilteo'],  # require this to be in the location/decr and address
    'Redondo': ['redondo'],
    'Titlow': ['titlow'],
    'Possession Point': ['possession point'],
    'Salt Creek': ['salt creek'],
    'Sund Rock': ['sund', 'rock'],
}
# tags that indicate non-dive activities to ignore
SKIP = ['friends of', 'club meet', 'sunset hill', 'lujac', 'boat', 'charter', 'long island', 'davidson rock', 'forum']

class Dive:
    # website data
    date = None  # dt object
    title = ""
    descr = ""
    location = ""
    address = ""

    # interpreted data
    splash = ""  # if able to get splash time, put it here
    site = ""
    slack = None  # Slack object

    def __str__(self):
        return '{}  {}  {}'.format(dt.strftime(self.date, MEETUP_TIME_FORMAT), self.title, self.location)

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

def getDataFileName():
    name = './dive_meetup_data.csv'
    filename = name
    i = 1
    while os.path.isfile(filename):
        filename = name.replace('data', 'data_' + str(i))
        i += 1
    return filename

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

# Iterates through main list element in given driver, writes dive data to file with given csv writer
def parseDives(d, w):
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
            date = text[3]
            title = text[4].lower()
            descr = text[7].lower()
            location = text[i + 1].lower()
            address = text[i + 2].lower()
            w.writerow([date, title, location, address, descr])

def appendMap(map, key, value):
    if key in map:
        map[key].append(value)
    else:
        map[key] = [value]

# Compares given str with the SITE_MAP tags for each site. Returns the name of the site if one is found
# and None if the given str doesn't match all the tags for any site.
def compareLocationTags(str, dive):
    for site, tags in SITE_MAP.items():
        foundAllTags = True
        for tag in tags:
            if tag not in str:
                foundAllTags = False
                break
        if foundAllTags:
            return site
    return None

# determines dive site for each of the given dives from SITE_MAP. Returns map from site -> {dives}
def refineDives(dives):
    results = {}
    for dive in dives:
        skip = False
        for str in SKIP:
            if str in dive.title or str in dive.location:
                appendMap(results, "Unclassified", dive)
                skip = True
                break
        if not skip:
            site = compareLocationTags(dive.location, dive)
            if not site:
                site = compareLocationTags(dive.title, dive)
            # if not site:
            #     site = compareLocationTags(dive.descr, dive)
            if not site:
                appendMap(results, "Unclassified", dive)
            else:
                appendMap(results, site, dive)
    return results


def main():
    getData = False
    if getData:
        d = webdriver.Firefox()
        d.get('https://secure.meetup.com/login')

        # Use cookie to login
        load_cookie(d, 'cookies.pkl')

        # Painful process of manual login
        # d.maximize_window()
        # data = json.loads(open('../personal_data.json').read())
        # elem = d.find_element_by_name("email")
        # elem.send_keys(data['meetup_username'])
        # elem = d.find_element_by_name("password")
        # elem.send_keys(data['meetup_password'])
        # input('Check "Im not a Robot box", then login. Enter any key to continue.')
        # save_cookie(d, 'cookies.pkl')

        d.get('https://www.meetup.com/Marker-Buoy-Dive-Club/events/past')

        scrollSeconds = 1200
        pauseSeconds = 7
        print('Scrolling for {}s. Content load pause = {}s'.format(scrollSeconds, pauseSeconds))
        scroll(d, pauseSeconds, scrollSeconds)

        print('Parsing web content and saving dive data to file')
        filename = getDataFileName()
        with open(filename, 'w', encoding='utf-8', newline='\n') as f:
            w = csv.writer(f, delimiter=',')
            parseDives(d, w)
        print('Data saved to file:', filename)
    else:
        # filename = getDataFileName()
        filename = 'dive_meetup_data.csv'


    print('Extracting dives from data file', filename)
    dives = []
    with open(filename, 'r', encoding='utf-8', newline='\n') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            dive = Dive()
            dive.date, dive.title, dive.location, dive.address, dive.descr = \
                dt.strptime(line[0], MEETUP_TIME_FORMAT), line[1], line[2], line[3], line[4]
            dives.append(dive)

    print('Classifying dive sites')
    results = refineDives(dives)

    # for site, vals in results.items():
    #     print(site)
    #     for dive in vals:
    #         print('\t', dive)

    print('Identifying the nearest period of slack current for each dive')
    json_data = open('dive_sites.json').read()
    data = json.loads(json_data)
    for site, sitedives in results.items():
        locationJson = None
        # find corresponding site in dive_sites.json
        for location in data["sites"]:
            if location['name'].lower() == site.lower():
                locationJson = location
                break
        if locationJson == None:
            print('ERROR: no location in dive_sites.json matched site:', site)
            continue
        # for each dive at this location, find the slack that was dove
        print(site)
        for dive in sitedives:
            # if site != "Sunrise Beach":
            if site != "Fox Island East Wall" and site != "Sunrise Beach":
                continue

            slacks = getSlacks(dive.date, locationJson['data'], daylight=True)  # TODO: ideally, this would not be limited to daylight
            estMeetupTimes = {}  # estimated meetup time for the slack -> slack
            for slack in slacks:
                times = getEntryTimes(slack, locationJson)
                if not times:
                    continue
                estMeetupTimes[times[1] - td(minutes=45)] = slack  # takes ~45min to meet and gear up
            # find the estMeetupTime closest to the actual meetup time. This gives the slack the dive was planned for.
            minDelta, slackDove = td(hours=99999).total_seconds(), None
            for estTime, slack in estMeetupTimes.items():
                diff = abs((dive.date - estTime).total_seconds())
                if diff < minDelta:
                    minDelta, slackDove = diff, slack

            dive.slack = slackDove
            print('\t', dive)
            # print('\t\t', slacks)
            print('\t\t', slackDove)
            minCurrentTime, markerBuoyEntryTime, entryTime = getEntryTimes(dive.slack, locationJson)
            minCurrentTime = dt.strftime(minCurrentTime, MEETUP_TIME_FORMAT)
            markerBuoyEntryTime = dt.strftime(markerBuoyEntryTime, MEETUP_TIME_FORMAT)
            entryTime = dt.strftime(entryTime, MEETUP_TIME_FORMAT)
            print('\t\tMarkerBuoyEntryTime = {} MyEntryTime = {} MinCurrentTime = {}'.format(markerBuoyEntryTime, entryTime, minCurrentTime))

    # filename = getDataFileName()
    # print('Writing slacks to file', filename)
    # with open(filename, 'w', encoding='utf-8', newline='\n') as f:
    #     w = csv.writer(f, delimiter=',')
    #     for dive in dives:
    #         w.writerow([dt.strftime(dive.date, MEETUP_TIME_FORMAT), dive.title, dive.location, dive.address, dive.descr, dive.slack])
    # print('Done writing to file', filename)





if __name__ == "__main__":
    main()
