#!/usr/bin/python
import rtc
import environment
import imu
import adc
import datetime
import time
import smbus
import ctypes

# Real time clock
real_time_clock = rtc.RealTimeClock()
#real_time_clock.SetTimeFromSystemClock()
real_time_clock.Update()
print real_time_clock.GetTimestamp()

# Environment sensor
'''environment_sensor = environment.EnvironmentSensor()
environment_sensor.ForceSingleMeasurement()
time.sleep(1)
environment_sensor.ReadCalibrationData()
environment_sensor.ReadRawMeasurementData()
environment_sensor.CalculateTemperature()
environment_sensor.CalculatePressure()
environment_sensor.CalculateHumidity()

print 'Temperature =', environment_sensor.GetTemperature()
print 'Pressure =', environment_sensor.GetPressure()
print 'Humidity =', environment_sensor.GetHumidity()'''

# IMU
inertial_measurement_unit = imu.InertialMeasurementUnit()
inertial_measurement_unit.Update()
print 'Acceleration =', inertial_measurement_unit.GetAcceleration()
print 'Gyrometer =', inertial_measurement_unit.GetGyrometer()
print 'Magnetometer =', inertial_measurement_unit.GetMagnetometer()

# ADC
analog_to_digital_converter = adc.AnalogToDigitalConverter()
analog_to_digital_converter.Update()
print analog_to_digital_converter.GetVoltages()
'''bus = smbus.SMBus(1)
print bus.read_word_data(0x08, 0b10001000)
bus.close()'''
