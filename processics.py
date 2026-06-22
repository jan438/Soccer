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
    
def select32(resultpoule):
    selected32 = resultpoule
    if resultpoule == "Winner A":
        selected32 = "Mexico"
    if resultpoule == "Winner B":
        selected32 = "Winner Bt"
    if resultpoule == "Winner C":
        selected32 = "Winner Ct"
    if resultpoule == "Winner D":
        selected32 = "V. Staten"
        
    if resultpoule == "Winner E":
        selected32 = "Duitsland"
    if resultpoule == "Winner F":
        selected32 = "Winner Ft"
    if resultpoule == "Winner G":
        selected32 = "Winner Gt"
    if resultpoule == "Winner H":
        selected32 = "Winner Ht"
        
    if resultpoule == "Winner I":
        selected32 = "Winner It"
    if resultpoule == "Winner J":
        selected32 = "Winner Jt"
    if resultpoule == "Winner K":
        selected32 = "Winner Kt"
    if resultpoule == "Winner L":
        selected32 = "Winner Lt"
        
    if resultpoule == "Runnerup A":
        selected32 = "Runnerup At"
    if resultpoule == "Runnerup B":
        selected32 = "Runnerup Bt"
    if resultpoule == "Runnerup C":
        selected32 = "Runnerup Ct"
    if resultpoule == "Runnerup D":
        selected32 = "Runnerup Dt"
        
    if resultpoule == "Runnerup E":
        selected32 = "Runnerup Et"
    if resultpoule == "Runnerup F":
        selected32 = "Runnerup Ft"
    if resultpoule == "Runnerup G":
        selected32 = "Runnerup Gt"
    if resultpoule == "Runnerup H":
        selected32 = "Runnerup Ht"
        
    if resultpoule == "Runnerup I":
        selected32 = "Runnerup It"
    if resultpoule == "Runnerup J":
        selected32 = "Runnerup Jt"
    if resultpoule == "Runnerup K":
        selected32 = "Runnerup Kt"
    if resultpoule == "Runnerup L":
        selected32 = "Runnerup Lt"
        
    if resultpoule == "3rd ABCDF":
        selected32 = "3rd ABCDFt"    
    if resultpoule == "3rd CDFGH":
        selected32 = "3rd CDFGHt"
    if resultpoule == "3rd CEFHI":
        selected32 = "3rd CEFHIt"
    if resultpoule == "3rd EHIJK":
        selected32 = "3rd EHIJKt"
        
    if resultpoule == "3rd AEHIJ":
        selected32 = "3rd AEHIJt"    
    if resultpoule == "3rd BEFIJ":
        selected32 = "3rd BEFIJt"
    if resultpoule == "3rd EFGIJ":
        selected32 = "3rd EFGIJt"    
    if resultpoule == "3rd DEIJL":
        selected32 = "3rd DEIJLt"
            
    return selected32
    
if sys.platform[0] == 'l':
    path = '/home/jan/git/Soccer'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Soccer"
os.chdir(path)
eventcal = "Calendar/WK2026new.ics"
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
    print(i, category)
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
        tzinfo=None
    )
    [houre, minutee] = converttimetztolocalclock(gameevents[i].endtime)
    e.end = datetime(
        year=2026,
        month=gameevents[i].month,
        day=gameevents[i].day,
        hour=hourb,
        minute=minuteb + 15,
        second=0,
        tzinfo=None
    )
    if category == "3":
        idx = e.description.find("-")
        opponent1 = e.description[:idx - 1]
        opponent2 = e.description[idx + 2:]
        opponent1 = select32(opponent1)
        opponent2 = select32(opponent2)
        e.description = opponent1 + " - " + opponent2
        count32 += 1
    c.events.add(e)

with open("Calendar/WK2026ics.ics", "w") as f:
    f.writelines(c)
    f.close()

key = input("Wait")
