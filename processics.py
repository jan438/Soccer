import os
from datetime import datetime, date, timedelta
import pytz
import os
import sys
import csv
import math
import unicodedata
from ics import Calendar, Event
from datetime import datetime, timezone, timedelta

alleventslines = []
gameevents = []
opponents32 = [
"00opponent",
"01opponent",
"02opponent",
"03opponent",
"04opponent",
"05opponent",
"06opponent",
"07opponent",
"08opponent",
"09opponent",
"10opponent",
"11opponent",
"12opponent",
"13opponent",
"14opponent",
"15opponent"
]

class GameEvent:
    def __init__(self, summary, day, description, location, starttime, endtime, month):
        self.summary = summary
        self.day = day
        self.description = description
        self.location = location
        self.starttime = starttime
        self.endtime = endtime
        self.month = month

def converttimetztolocalclock(timetz):
    utc_string = timetz
    utc_format = "%Y%m%dT%H%M%S"
    local_tz = pytz.timezone('Europe/Amsterdam')
    utc_dt = datetime.strptime(utc_string, utc_format)
    local_dt = utc_dt
    hour = local_dt.hour
    minute = local_dt.minute
    return [hour, minute]
    
if sys.platform[0] == 'l':
    path = '/home/jan/git/Soccer'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Soccer"
os.chdir(path)
eventcal = "Calendar/WK2026.ics"
in_file = open(os.path.join(path, eventcal), 'r')
count = 0
lastpos = 0
count32 = 0
for line in in_file:
    newlinepos = line.find("\t\n")
    lastsubstring = line[lastpos:newlinepos]
    alleventslines.append(lastsubstring)
    count += 1
in_file.close()
print("Count eventslines", len(alleventslines))
for i in range(len(alleventslines)):
    neweventpos = alleventslines[i].find("BEGIN:VEVENT")
    summaryeventpos = alleventslines[i].find("SUMMARY")
    descriptioneventpos = alleventslines[i].find("DESCRIPTION")
    locationeventpos = alleventslines[i].find("LOCATION")
    dtstarteventpos = alleventslines[i].find("DTSTART")
    dtendeventpos = alleventslines[i].find("DTEND")
    endeventpos = alleventslines[i].find("END:VEVENT")
    if neweventpos == 0:
        day = 0
        description = ""
        location = ""
        starttime = 0
        endtime = 0
        month = 0
    if dtstarteventpos == 0:
        eventdtstartstr = alleventslines[i][8:]
        datevaluepos = alleventslines[i].find("VALUE=DATE:")
        if datevaluepos == 8:
            eventdtstartstr = alleventslines[i][19:]
        year = int(eventdtstartstr[:4])
        month = int(eventdtstartstr[4:6])
        day = int(eventdtstartstr[6:8])
        starttime = eventdtstartstr
    if dtendeventpos == 0:
        endtime = alleventslines[i][6:]
    if summaryeventpos == 0:
        summary = alleventslines[i][8:]
    if descriptioneventpos == 0:
        description = alleventslines[i][12:]
    if locationeventpos == 0:
        location = alleventslines[i][9:]
    if endeventpos == 0:
        gameevents.append(GameEvent(summary, day, description, location, starttime, endtime, month))
print("Count game events", len(gameevents))

c = Calendar()
for i in range(len(gameevents)):
    e = Event()
    e.name = gameevents[i].summary
    if len(e.name) == 2:
        category = e.name[0]
    else:
        category = e.name[5]
    opponent1 = ""
    opponent2 = ""
    e.description = gameevents[i].description
    e.location = gameevents[i].location
    [hourb, minuteb] = converttimetztolocalclock(gameevents[i].starttime)
    e.begin = datetime(
        year=2026,
        month=gameevents[i].month,
        day=gameevents[i].day,
        hour=hourb,
        minute=minuteb,
        second=0,
        tzinfo=timezone(timedelta(seconds=7200))
    )
    [houre, minutee] = converttimetztolocalclock(gameevents[i].endtime)
    e.end = datetime(
        year=2026,
        month=gameevents[i].month,
        day=gameevents[i].day,
        hour=hourb,
        minute=minuteb + 15,
        second=0,
        tzinfo=timezone(timedelta(seconds=7200))
    )
    if category == "3":
        idx = e.description.find("-")
        opponent1 = e.description[:idx - 1]
        opponent2 = e.description[idx + 2:]
        e.description = opponent1 + " - " + opponent2
        print(count32, e.description, opponents32[count32])
        count32 += 1
    c.events.add(e)

with open("PDF/WK2026_32.ics", "w") as f:
    f.writelines(c)
    f.close()

key = input("Wait")
