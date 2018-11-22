#!/usr/bin/python
import time
import smbus
import ctypes
from math import *

class InertialMeasurementUnit:
    def __init__(self):
        self.InitializeDevice()

    # High level functions
    def Update(self):
        self.UpdateMeasurementData()

    def GetAcceleration(self):
        return self.accel

    def GetGyrometer(self):
        return self.gyro

    def GetMagnetometer(self):
        return self.mag

    # Low level functions
    def InitializeDevice(self):
        bus = smbus.SMBus(1)
        bus.write_byte_data(0x69, 0x40, 0b00010101)
        bus.write_byte_data(0x69, 0x41, 0b00000011)
        bus.write_byte_data(0x69, 0x43, 0b00000100)
        bus.write_byte_data(0x69, 0x44, 0b00000011)
        bus.write_byte_data(0x69, 0x4C, 0b00000000)
        bus.write_byte_data(0x69, 0x7E, 0x11)
        bus.write_byte_data(0x69, 0x7E, 0x15)
        bus.write_byte_data(0x69, 0x7E, 0x19)
        bus.close()

    def UpdateMeasurementData(self):
        bus = smbus.SMBus(1)
        self.raw_measurement_data = bus.read_i2c_block_data(0x69, 0x04, 20)
        print bin(bus.read_byte_data(0x69, 0x03))
        print bin(bus.read_byte_data(0x69, 0x1B))
        bus.close()

        self.accel[2] = round(ctypes.c_short((self.raw_measurement_data[19]<<8) | self.raw_measurement_data[18]).value * 2.0 / 2**15, 2)
        self.accel[1] = round(ctypes.c_short((self.raw_measurement_data[17]<<8) | self.raw_measurement_data[16]).value * 2.0 / 2**15, 2)
        self.accel[0] = round(ctypes.c_short((self.raw_measurement_data[15]<<8) | self.raw_measurement_data[14]).value * 2.0 / 2**15, 2)

        self.gyro[2] = round(ctypes.c_short((self.raw_measurement_data[13]<<8) | self.raw_measurement_data[12]).value * 125.0 / 2**15, 2)
        self.gyro[1] =  round(ctypes.c_short((self.raw_measurement_data[11]<<8) | self.raw_measurement_data[10]).value * 125.0 / 2**15, 2)
        self.gyro[0] =  round(ctypes.c_short((self.raw_measurement_data[9]<<8) | self.raw_measurement_data[8]).value * 125.0 / 2**15, 2)

        self.mag[2] = ctypes.c_short((self.raw_measurement_data[5]<<8) | self.raw_measurement_data[4]).value
        self.mag[1] =  ctypes.c_short((self.raw_measurement_data[3]<<8) | self.raw_measurement_data[2]).value
        self.mag[0] =  ctypes.c_short((self.raw_measurement_data[1]<<8) | self.raw_measurement_data[0]).value


    # Register data
    raw_measurement_data = [ 0x00 ] * 20
    accel = [ 0.00, 0.00, 0.00 ]
    gyro = [ 0.00, 0.00, 0.00 ]
    mag = [ 0.00, 0.00, 0.00 ]
