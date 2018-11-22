#!/usr/bin/python
import rtc
import environment
import datetime
import time

# Real time clock
real_time_clock = rtc.RealTimeClock()
#real_time_clock.SetTimeFromSystemClock()
real_time_clock.Update()
print real_time_clock.GetTimestamp()

# Environment sensor
environment_sensor = environment.EnvironmentSensor()
environment_sensor.ForceSingleMeasurement()
time.sleep(1)
environment_sensor.ReadCalibrationData()
environment_sensor.ReadRawMeasurementData()
environment_sensor.CalculateTemperature()
environment_sensor.CalculatePressure()
environment_sensor.CalculateHumidity()

print "Temperature =", environment_sensor.GetTemperature()
print "Pressure =", environment_sensor.GetPressure()
print "Humidity =", environment_sensor.GetHumidity()
