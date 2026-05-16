from datetime import datetime, date, timedelta
utc_string = "20260613T220000"
utc_format = "%Y%m%dT%H%M%S"
utc_dt = datetime.strptime(utc_string, utc_format)
local_dt = utc_dt
hour = local_dt.hour
minute = local_dt.minute
print(utc_dt, hour, minute)

key = input("Wait")
