#!/usr/bin/python
import rtc
import environment
import datetime

# Real time clock
real_time_clock = rtc.RealTimeClock()
real_time_clock.Update()
print real_time_clock.GetTimestamp()

# Environment sensor
environment_sensor = environment.EnvironmentSensor()
environment_sensor.ForceSingleMeasurement()
