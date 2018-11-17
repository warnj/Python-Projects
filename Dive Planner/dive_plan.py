import urllib.request, datetime, json
from pandas.tseries.holiday import USFederalHolidayCalendar
from bs4 import BeautifulSoup

class Slack:
    time = None
    slackBeforeEbb = False
    ebbSpeed = 0.0
    floodSpeed = 0.0

    def __str__(self):
        if self.slackBeforeEbb:
            return str(self.floodSpeed) + ' -> ' + datetime.datetime.strftime(self.time, '%Y-%m-%d %I:%M%p') + ' -> ' + str(self.ebbSpeed)
        else:
            return str(self.ebbSpeed) + ' -> ' + datetime.datetime.strftime(self.time, '%Y-%m-%d %I:%M%p') + ' -> ' + str(self.floodSpeed)

    def __repr__(self):
        return self.__str__()

# returns a list of datetime days that are weekends and holiday that occur between now and futureDays in the future
def getNonWorkDays(futureDays):
    start = datetime.date.today()
    start = datetime.datetime(start.year, start.month, start.day)
    end = start + datetime.timedelta(days=futureDays)

    cal = USFederalHolidayCalendar()  # does not include some business holidays like black friday
    holidays = cal.holidays(start=start, end=end).to_pydatetime()

    delta = datetime.timedelta(days=1)
    d = start
    workdays = {0,1,2,3,4}
    nonWorkDays = []
    while d <= end:
        if d.weekday() not in workdays:
            nonWorkDays.append(d)
        elif d in holidays:
            nonWorkDays.append(d)
        d += delta
    return nonWorkDays

# returns a list of datetime days that occur between now and futureDays in the future
def getAllDays(futureDays):
    start = datetime.date.today()
    start = datetime.datetime(start.year, start.month, start.day)
    end = start + datetime.timedelta(days=futureDays)
    delta = datetime.timedelta(days=1)
    d = start
    days = []
    while d <= end:
        days.append(d)
        d += delta
    return days

# returns list with indexes of the daytime slack currents in the given list of data lines
def getDaySlacks(lines):
    sunrise = False
    slacks = []
    for i, line in enumerate(lines):
        if sunrise and "Slack" in line:
            slacks.append(i)
        elif "Sunrise" in line:
            sunrise = i
        elif "Sunset" in line:
            break
    return slacks

# returns a list of Slack objects corresponding to the slack indexes within the list of data lines
def getSlackData(lines, indexes):
    slacks = []
    for i in indexes:
        s = Slack()

        pre = i-1
        while "Ebb" not in lines[pre] and "Flood" not in lines[pre]:
            pre -= 1
        s.slackBeforeEbb = "Flood" in lines[pre]
        tokens1 = lines[pre].split()

        post = i+1
        while "Ebb" not in lines[post] and "Flood" not in lines[post]:
            post += 1
        tokens2 = lines[post].split()

        if s.slackBeforeEbb:
            s.floodSpeed = float(tokens1[5])
            s.ebbSpeed = float(tokens2[5])
        else:
            s.ebbSpeed = float(tokens1[5])
            s.floodSpeed = float(tokens2[5])

        tokens = lines[i].split()
        dayTimeStr = tokens[0] + " " + tokens[2] + tokens[3] # ex: 2018-11-17 1:15PM
        s.time = datetime.datetime.strptime(dayTimeStr, '%Y-%m-%d %I:%M%p')
        slacks.append(s)
    return slacks

# prints entry time for Slack s at the given site
def printDive(s, site):
    if s.slackBeforeEbb:
        delta = datetime.timedelta(minutes=site["slack_before_ebb"])
    else:
        delta = datetime.timedelta(minutes=site["slack_before_flood"])
    minCurrentTime = s.time + delta
    entryTime = minCurrentTime - datetime.timedelta(minutes=site["dive_duration"] / 2) - datetime.timedelta(minutes=site["surface_swim_time"])
    print('\tDiveable: ' + str(s))
    print('\t\tConsidering factors: MinCurrentTime = {}, DiveDuration = {}, SurfaceSwimTime = {}'.format(minCurrentTime, site["dive_duration"], site["surface_swim_time"]))
    print('\t\tEntrytime: ' + datetime.datetime.strftime(entryTime, '%Y-%m-%d %I:%M%p'))
    print('\t\tMarker Buoy Entrytime (60min dive, no surface swim): ' + datetime.datetime.strftime(
        minCurrentTime - datetime.timedelta(minutes=30), '%Y-%m-%d %I:%M%p'))

# Checks the givens list of Slacks if a dive is possible. If so, prints information about the dive.
def printDiveDay(slacks, site):
    for s in slacks:
        assert s.ebbSpeed < 0.0
        assert s.floodSpeed > 0.0
        # Check if diveable or not
        if s.slackBeforeEbb and not site["diveable_before_ebb"]:
            print('\t' + str(s) + '\t Not diveable before ebb')
        elif not s.slackBeforeEbb and not site["diveable_before_flood"]:
            print('\t' + str(s) + '\t Not diveable before flood')
        elif site["diveable_off_slack"] and (s.floodSpeed < site["max_diveable_flood"] or abs(s.ebbSpeed) < site["max_diveable_ebb"]):
            print('\t' + str(s) + '\t Diveable off slack')
            printDive(s, site)
        elif s.floodSpeed > site["max_flood"] or abs(s.ebbSpeed) > abs(site["max_ebb"]) or s.floodSpeed + abs(s.ebbSpeed) > site["max_total_speed"]:
            print('\t' + str(s) + '\t Current too strong')
        else:
            printDive(s, site)



DAYS_IN_FUTURE = 150
SITES = {"Deception Pass"}
filterNonWorkDays = True
filterDaylight = True




if filterNonWorkDays:
    possibleDiveDays = getNonWorkDays(DAYS_IN_FUTURE)
else:
    possibleDiveDays = getAllDays(DAYS_IN_FUTURE)

json_data = open('dive_sites.json').read()
data = json.loads(json_data)

for i in range(len(data["sites"])):
    siteData = data["sites"][i]
    if siteData["name"] not in SITES:
        continue
    print(siteData["name"])
    for day in possibleDiveDays:
        url = siteData["data"] + "?y={}&m={}&d={}".format(day.year, day.month, day.day)
        with urllib.request.urlopen(url) as response:
           html = response.read()
           soup = BeautifulSoup(html, 'html.parser')
           predictions = soup.find("pre", {"class": "predictions-table"})
           lines = predictions.text.splitlines()

           slackIndexes = getDaySlacks(lines)
           # print("Slack indexes", slackIndexes)
           # for i in slackIndexes:
           #     print(lines[i])

           slacks = getSlackData(lines, slackIndexes)
           # print("Slack objects", slacks)

           printDiveDay(slacks, siteData)


