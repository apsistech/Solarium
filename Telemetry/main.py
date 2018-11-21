#!/usr/bin/python
import rtc
import datetime

real_time_clock = rtc.RealTimeClock()

#real_time_clock.Update()
real_time_clock.SetTimeFromTimestamp(datetime.datetime.utcnow().isoformat())
