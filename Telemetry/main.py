#!/usr/bin/python
import rtc
import environment
import datetime
import time
import smbus
import ctypes

'''# Real time clock
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
print "Humidity =", environment_sensor.GetHumidity()'''

# IMU
bus = smbus.SMBus(1)
print hex(bus.read_byte_data(0x69, 0x00))
bus.write_byte_data(0x69, 0x40, 0b0010101)
bus.write_byte_data(0x69, 0x41, 0b0000011)
bus.write_byte_data(0x69, 0x7E, 0x11)
bus.write_byte_data(0x69, 0x7E, 0x15)
bus.write_byte_data(0x69, 0x7E, 0x19)
raw_measurement_data = bus.read_i2c_block_data(0x69, 0x04, 20)
print ctypes.c_short((raw_measurement_data[19]<<8) | raw_measurement_data[18]).value * 2.0 / 2**15
print ctypes.c_short((raw_measurement_data[17]<<8) | raw_measurement_data[16]).value * 2.0 / 2**15
print ctypes.c_short((raw_measurement_data[15]<<8) | raw_measurement_data[14]).value * 2.0 / 2**15
bus.close()
