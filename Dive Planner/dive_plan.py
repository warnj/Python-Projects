import urllib.request, datetime, json
from pandas.tseries.holiday import USFederalHolidayCalendar
from bs4 import BeautifulSoup
from datetime import datetime as dt
from datetime import timedelta as td

TIMEPARSEFMT = '%Y-%m-%d %I:%M%p'  # example: 2019-01-18 09:36AM
TIMEPRINTFMT = '%a %Y-%m-%d %I:%M%p'  # example: Fri 2019-01-18 09:36AM

class Slack:
    time = None
    sunriseTime = None
    sunsetTime = None  # this is never used, but might be interesting to print it sometimes
    slackBeforeEbb = False
    ebbSpeed = 0.0
    floodSpeed = 0.0

    def __str__(self):
        if self.slackBeforeEbb:
            return '{} -> {} -> {}'.format(self.floodSpeed, dt.strftime(self.time, TIMEPRINTFMT), self.ebbSpeed)
        else:
            return '{} -> {} -> {}'.format(self.ebbSpeed, dt.strftime(self.time, TIMEPRINTFMT), self.floodSpeed)

    def __repr__(self):
        return self.__str__()


def printinfo(str):
    if PRINTINFO:
        print(str)


def createOrAppend(str):
    global SITES
    if SITES:
        SITES.add(str)
    else:
        SITES = {str}


# returns a list of datetime days that are weekends and holiday that occur between start (today by default) and
# futureDays in the future
def getNonWorkDays(futureDays, start=dt.now()):
    start = dt(start.year, start.month, start.day)
    end = start + td(days=futureDays)

    cal = USFederalHolidayCalendar()  # does not include some business holidays like black friday
    holidays = cal.holidays(start=start, end=end).to_pydatetime()

    delta = td(days=1)
    d = start
    workdays = {0, 1, 2, 3, 4}
    nonWorkDays = []
    while d <= end:
        if d.weekday() not in workdays:
            nonWorkDays.append(d)
        elif d in holidays:
            nonWorkDays.append(d)
        d += delta
    return nonWorkDays


# returns a list of datetime days that occur between start (today by default) and futureDays in the future
def getAllDays(futureDays, start=dt.now()):
    start = dt(start.year, start.month, start.day)
    end = start + td(days=futureDays)
    delta = td(days=1)
    d = start
    days = []
    while d <= end:
        days.append(d)
        d += delta
    return days


# Returns list with indexes of the daytime slack currents in the given list of data lines. Also returns sunrise time
# and sunset time.
def getDaySlacks(lines):
    sunrise = None
    slacks = []
    for i, line in enumerate(lines):
        if sunrise and "Slack" in line:
            slacks.append(i)
        elif "Sunrise" in line:
            tokens = line.split()
            dayTimeStr = tokens[0] + " " + tokens[1] + tokens[2]  # ex: 2018-11-17 1:15PM
            sunrise = dt.strptime(dayTimeStr, TIMEPARSEFMT)
        elif "Sunset" in line:
            tokens = line.split()
            dayTimeStr = tokens[0] + " " + tokens[1] + tokens[2]  # ex: 2018-11-17 1:15PM
            sunset = dt.strptime(dayTimeStr, TIMEPARSEFMT)
            return slacks, sunrise, sunset
    return slacks, sunrise, None


# returns list with indexes of the slack currents in the first 24hrs of the given list of data lines
def getAllSlacks(lines):
    weekday = lines[0].split()[1]
    slacks = []
    for i, line in enumerate(lines):
        if line.split()[1] != weekday:
            return slacks
        elif "Slack" in line:
            slacks.append(i)
    return slacks


# returns a list of Slack objects corresponding to the slack indexes within the list of data lines
def getSlackData(lines, indexes, sunrise, sunset):
    slacks = []
    for i in indexes:
        s = Slack()
        s.sunriseTime = sunrise
        s.sunsetTime = sunset

        pre = i - 1
        while "Ebb" not in lines[pre] and "Flood" not in lines[pre]:
            pre -= 1
        s.slackBeforeEbb = "Flood" in lines[pre]
        tokens1 = lines[pre].split()

        post = i + 1
        while "Ebb" not in lines[post] and "Flood" not in lines[post]:
            post += 1
        tokens2 = lines[post].split()

        if s.slackBeforeEbb:
            s.floodSpeed = float(tokens1[4])
            s.ebbSpeed = float(tokens2[4])
        else:
            s.ebbSpeed = float(tokens1[4])
            s.floodSpeed = float(tokens2[4])

        tokens = lines[i].split()
        dayTimeStr = tokens[0] + " " + tokens[1] + tokens[2]  # ex: 2018-11-17 1:15PM
        s.time = dt.strptime(dayTimeStr, TIMEPARSEFMT)
        slacks.append(s)
    return slacks


# Returns a list of slacks from given mobilegeographics url on the given day. Includes night slacks if daylight=False
def getSlacks(day, baseUrl, daylight=True):
    url = baseUrl + "?y={}&m={}&d={}".format(day.year, day.month, day.day)
    with urllib.request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        predictions = soup.find("pre", {"class": "predictions-table"})
        lines = predictions.text.splitlines()[3:]

        sunrise = None
        sunset = None
        if daylight:
            slackIndexes, sunrise, sunset = getDaySlacks(lines)
        else:
            slackIndexes = getAllSlacks(lines)
        return getSlackData(lines, slackIndexes, sunrise, sunset)  # populate Slack objects


# Returns [mincurrenttime, markerbuoyentrytime, myentrytime] for the given slack at the given site
# mincurrenttime = time of slack current, markerbuoyentrytime = 30min before mincurrenttime,
# myentrytime = mincurrenttime - surfaceswimtime - expecteddivetime/2
# Returns None if an expected json data point is not found
def getEntryTimes(s, site):
    try:
        if s.slackBeforeEbb:
            delta = td(minutes=site["slack_before_ebb"])
        else:
            delta = td(minutes=site["slack_before_flood"])
        minCurrentTime = s.time + delta
        entryTime = minCurrentTime - td(minutes=site["dive_duration"] / 2) - td(minutes=site["surface_swim_time"])
        markerBuoyEntryTime = minCurrentTime - td(minutes=30)
        return minCurrentTime, markerBuoyEntryTime, entryTime
    except KeyError:
        return None


# Prints entry time for Slack s at the given site
def printDive(s, site):
    times = getEntryTimes(s, site)
    if not times:
        print('ERROR: a json key was expected that was not found')
    else:
        minCurrentTime, markerBuoyEntryTime, entryTime = times
        if s.sunriseTime:
            warning = ""
            if entryTime < s.sunriseTime:
                warning = 'BEFORE'
            elif entryTime - td(minutes=30) < s.sunriseTime:
                warning = 'near'
            if warning:
                print('\tWARNING: entry time of {} is {} sunrise at {}'.format(dt.strftime(entryTime, TIMEPRINTFMT),
                    warning, dt.strftime(s.sunriseTime, TIMEPRINTFMT)))

        print('\tDiveable: ' + str(s))
        print('\t\tMinCurrentTime = {}, Duration = {}, SurfaceSwim = {}'
                .format(dt.strftime(minCurrentTime, TIMEPRINTFMT), site["dive_duration"], site["surface_swim_time"]))
        print('\t\tEntrytime: ' + dt.strftime(entryTime, TIMEPRINTFMT))
        print('\t\tMarker Buoy Entrytime (60min dive, no surface swim):', dt.strftime(markerBuoyEntryTime, TIMEPRINTFMT))


# Checks the givens list of Slacks if a dive is possible. If so, prints information about the dive.
def printDiveDay(slacks, site):
    for s in slacks:
        assert s.ebbSpeed <= 0.0
        assert s.floodSpeed >= 0.0
        # Check if diveable or not
        if s.slackBeforeEbb and not site["diveable_before_ebb"]:
            printinfo('\t' + str(s) + '\t Not diveable before ebb')
        elif not s.slackBeforeEbb and not site["diveable_before_flood"]:
            printinfo('\t' + str(s) + '\t Not diveable before flood')
        elif site["diveable_off_slack"] and \
                (s.floodSpeed < site["max_diveable_flood"] or abs(s.ebbSpeed) < site["max_diveable_ebb"]):
            print('\t' + str(s) + '\t Diveable off slack')
            printDive(s, site)
        elif s.floodSpeed > site["max_flood"] or abs(s.ebbSpeed) > abs(site["max_ebb"]) or \
                s.floodSpeed + abs(s.ebbSpeed) > site["max_total_speed"]:
            printinfo('\t' + str(s) + '\t Current too strong')
        else:
            printDive(s, site)


# ---------------------------------- CONFIGURABLE PARAMETERS -----------------------------------------------------------
# START = dt.now()
START = dt(2019, 1, 16)  # date to begin considering diveable conditions
DAYS_IN_FUTURE = 2  # number of days after START to consider

SITES = None  # Consider all sites
# createOrAppend("Salt Creek")
# createOrAppend("Deception Pass")
# createOrAppend("Skyline Wall")
# createOrAppend("Keystone Jetty")
# createOrAppend("Possession Point")
# createOrAppend("Mukilteo")
# createOrAppend("Edmonds Underwater Park")
# createOrAppend("Three Tree North")
# createOrAppend("Alki Pipeline or Junkyard")
# createOrAppend("Saltwater State Park")
createOrAppend("Day Island Wall")
# createOrAppend("Sunrise Beach")
# createOrAppend("Fox Island Bridge")
# createOrAppend("Fox Island East Wall")
# createOrAppend("Titlow")


filterNonWorkDays = False  # only consider diving on weekends and holidays
filterDaylight = True  # TODO: fix unimportant bug with this filter if first slack of the day (well before sunrise) doesn't have a previous Max before it, loops around to future with negative index

PRINTINFO = True  # print non-diveable days and reason why not diveable

possibleDiveDays = None  # Specify dates
possibleDiveDays = [
    # dt(2016, 11, 5),
    # dt(2016, 3, 5),
    # dt(2014, 6, 7)
    # dt(2019, 1, 19),
    # dt(2018, 12, 27)
]
# ----------------------------------------------------------------------------------------------------------------------

def main():
    global possibleDiveDays

    if not possibleDiveDays:
        if filterNonWorkDays:
            possibleDiveDays = getNonWorkDays(DAYS_IN_FUTURE, START)
        else:
            possibleDiveDays = getAllDays(DAYS_IN_FUTURE, START)

    json_data = open('dive_sites.json').read()
    data = json.loads(json_data)

    for i in range(len(data["sites"])):
        siteData = data["sites"][i]
        if SITES and siteData["name"] not in SITES:
            continue
        print(siteData["name"])
        for day in possibleDiveDays:
            slacks = getSlacks(day, siteData["data"], daylight=filterDaylight)
            printDiveDay(slacks, siteData)  # interpret Slack objects with json data to identify diveable times


if __name__ == "__main__":
    main()
