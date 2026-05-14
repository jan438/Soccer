from datetime import datetime, timezone, timedelta
from ics import Calendar, Event

c = Calendar()
e = Event()
e.summary = "My cool event"
e.description = "A meaningful description"
e.begin = datetime.fromisoformat("2022-06-06T12:05:23+02:00")
e.end = datetime(
    year=2022,
    month=6,
    day=6,
    hour=12,
    minute=5,
    second=23,
    tzinfo=timezone(timedelta(seconds=7200)),
)
c.events.add(e)

key = input("Wait")
