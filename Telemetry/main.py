#!/usr/bin/python
import rtc
import datetime

real_time_clock = rtc.RealTimeClock()

real_time_clock.Update()
print real_time_clock.GetTimestamp()
