#!/usr/bin/python
import smbus

class EnvironmentSensor:
    def __init__(self):
        pass

    # Low level functions
    def ForceSingleMeasurement(self):
        bus = smbus.SMBus(1)
        bus.write_byte_data(0x76, 0xF2, 0b00000001)
        bus.write_byte_data(0x76, 0xF4, 0b00100101)
        print bus.read_i2c_block_data(0x76, 0xF2, 12)
        bus.close()
