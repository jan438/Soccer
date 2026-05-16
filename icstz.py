from dateutil.tz import gettz
from datetime import datetime as dt
from ics import Event, Calendar
import os, time
import pytz

t = dt(2020, 4, 1, 18, 0)
e = Event()
e.begin = t.replace(tzinfo=gettz('America/New York'))
e.begin

print(e)

key = input("Wait")
