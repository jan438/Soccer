from dateutil.tz import gettz
from datetime import datetime as dt
from ics import Event, Calendar
import os, time
import pytz

alleventslines = []
gameevents = []

class GameEvent:
    def __init__(self, summary, day, description, location, starttime, endtime, month):
        self.summary = summary
        self.day = day
        self.description = description
        self.location = location
        self.starttime = starttime
        self.endtime = endtime
        self.month = month
        
c = Calendar()
t = dt(2020, 4, 1, 18, 0)
e = Event(begin=t)

c.events.add(e)

with open("Calendar/WK2026_test_lines.ics", "w") as f:
    f.writelines(c)
    f.close()
    
c = Calendar()
count = 0
lastpos = 0

with open("Calendar/WK2026_test_lines.ics", "r") as f:
    for line in f:
        newlinepos = line.find("\t\n")
        lastsubstring = line[lastpos:newlinepos]
        alleventslines.append(lastsubstring)
        count += 1
    f.close()
    
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
        summary = ""
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
        eventdtendstr = alleventslines[i][6:]
        endtime = eventdtendstr[9:11] + ':' + eventdtendstr[11:13]
    if summaryeventpos == 0:
        summary = alleventslines[i][8:]
    if descriptioneventpos == 0:
        description = alleventslines[i][12:]
    if locationeventpos == 0:
        location = alleventslines[i][9:]
    if endeventpos == 0:
        gameevents.append(GameEvent(summary, day, description, location, starttime, endtime, month))
        
print(len(gameevents), gameevents[0].starttime)
         
key = input("Wait")
