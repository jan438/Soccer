from dateutil.tz import gettz
from datetime import datetime as dt
from ics import Event, Calendar
import os, time
import pytz

c = Calendar()
t = dt(2020, 4, 1, 18, 0)
e = Event(begin=t)

c.events.add(e)

with open("Calendar/WK2026_test_lines.ics", "w") as f:
    f.writelines(c)
    f.close()
    
c = Calendar()

with open("Calendar/WK2026_test_lines.ics", "r") as f:
    c = f.readlines()
    f.close()

key = input("Wait")
