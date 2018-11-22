#!/usr/bin/python
import smbus
import ctypes

class EnvironmentSensor:
    def __init__(self):
        pass

    # High level functions
    def Update(self):
        pass

    def GetTemperature(self):
        return self.temperature

    # Low level functions
    def ForceSingleMeasurement(self):
        bus = smbus.SMBus(1)
        bus.write_byte_data(0x76, 0xF2, 0b00000001)
        bus.write_byte_data(0x76, 0xF4, 0b00100101)
        #print bus.read_i2c_block_data(0x76, 0xF2, 12)
        bus.close()

    def ReadRawMeasurementData(self):
        bus = smbus.SMBus(1)
        self.raw_measurement_data = bus.read_i2c_block_data(0x76, 0xF7, 8)
        bus.close()

        print self.raw_measurement_data

        self.pressure_raw = (self.raw_measurement_data[0] << 12) \
                            + (self.raw_measurement_data[1] << 4) \
                            + (self.raw_measurement_data[2] >> 4)

        self.temperature_raw = (self.raw_measurement_data[3] << 12) \
                            + (self.raw_measurement_data[4] << 4) \
                            + (self.raw_measurement_data[5] >> 4)

        self.humidity_raw = (self.raw_measurement_data[6] << 8) \
                            + self.raw_measurement_data[7]


        print 'temperature_raw =', self.temperature_raw
        print 'pressure_raw =', self.pressure_raw
        print 'humidity_raw =', self.humidity_raw

    def ReadCalibrationData(self):
        bus = smbus.SMBus(1)
        self.calibration_data[0:26] = bus.read_i2c_block_data(0x76, 0x88, 26)
        self.calibration_data[26:42] = bus.read_i2c_block_data(0x76, 0xE1, 16)
        bus.close()

        self.dig_T1 = ctypes.c_ushort(self.calibration_data[0] | (self.calibration_data[1]<<8)).value
        self.dig_T2 = ctypes.c_short(self.calibration_data[2] | (self.calibration_data[3]<<8)).value
        self.dig_T3 = ctypes.c_short(self.calibration_data[4] | (self.calibration_data[5]<<8)).value
        self.dig_P1 = ctypes.c_ushort(self.calibration_data[6] | (self.calibration_data[7]<<8)).value
        self.dig_P2 = ctypes.c_short(self.calibration_data[8] | (self.calibration_data[9]<<8)).value
        self.dig_P3 = ctypes.c_short(self.calibration_data[10] | (self.calibration_data[11]<<8)).value
        self.dig_P4 = ctypes.c_short(self.calibration_data[12] | (self.calibration_data[13]<<8)).value
        self.dig_P5 = ctypes.c_short(self.calibration_data[14] | (self.calibration_data[15]<<8)).value
        self.dig_P6 = ctypes.c_short(self.calibration_data[16] | (self.calibration_data[17]<<8)).value
        self.dig_P7 = ctypes.c_short(self.calibration_data[18] | (self.calibration_data[19]<<8)).value
        self.dig_P8 = ctypes.c_short(self.calibration_data[20] | (self.calibration_data[21]<<8)).value
        self.dig_P9 = ctypes.c_short(self.calibration_data[22] | (self.calibration_data[23]<<8)).value
        self.dig_H1 = ctypes.c_ubyte(self.calibration_data[24]).value
        self.dig_H2 = ctypes.c_short(self.calibration_data[25] | (self.calibration_data[26]<<8)).value
        self.dig_H3 = ctypes.c_ubyte(self.calibration_data[27]).value
        self.dig_H4 = ctypes.c_short(self.calibration_data[28] | (self.calibration_data[29]<<8)).value
        self.dig_H5 = ctypes.c_short(self.calibration_data[30] | (self.calibration_data[31]<<8)).value
        self.dig_H6 = ctypes.c_byte(self.calibration_data[32]).value

        print 'dig_T1 =', self.dig_T1
        print 'dig_T2 =', self.dig_T2
        print 'dig_T3 =', self.dig_T3
        print 'dig_P1 =', self.dig_P1
        print 'dig_P2 =', self.dig_P2
        print 'dig_P3 =', self.dig_P3
        print 'dig_P4 =', self.dig_P4
        print 'dig_P5 =', self.dig_P5
        print 'dig_P6 =', self.dig_P6
        print 'dig_P7 =', self.dig_P7
        print 'dig_P8 =', self.dig_P8
        print 'dig_P9 =', self.dig_P9
        print 'dig_H1 =', self.dig_H1
        print 'dig_H2 =', self.dig_H2
        print 'dig_H3 =', self.dig_H3
        print 'dig_H4 =', self.dig_H4
        print 'dig_H5 =', self.dig_H5
        print 'dig_H6 =', self.dig_H6

    def CalculateTemperature(self):
        var1 = ((float(self.temperature_raw)/16384.0) - ((float(self.dig_T1)/1024.0))) * float(self.dig_T2)
        var2 = ((float(self.temperature_raw)/131072.0) - (float(self.dig_T1)/8192.00)) * ((float(self.temperature_raw)/1310720.0) - ((float(self.dig_T1)/8192.0) * float(self.dig_T3)))
        t_fine = var1 + var2
        
        self.temperature = (var1 + var2) / 5120.0

    # Register level data
    calibration_data = [ 0x00 ] * 42

    dig_T1 = 0x0000 # unsigned short
    dig_T2 = 0x0000 # signed short
    dig_T3 = 0x0000 # signed short
    dig_P1 = 0x0000 # unsigned short
    dig_P2 = 0x0000 # signed short
    dig_P3 = 0x0000 # signed short
    dig_P4 = 0x0000 # signed short
    dig_P5 = 0x0000 # signed short
    dig_P6 = 0x0000 # signed short
    dig_P7 = 0x0000 # signed short
    dig_P8 = 0x0000 # signed short
    dig_P9 = 0x0000 # signed short
    dig_H1 = 0x00   # unsigned char
    dig_H2 = 0x0000 # signed short
    dig_H3 = 0x00   # unsigned char
    dig_H4 = 0x0000 # signed short
    dig_H5 = 0x0000 # signed short
    dig_H6 = 0x00   # signed char

    raw_measurement_data = [ 0x00 ] * 9

    temperature_raw = 0x000000
    pressure_raw = 0x000000
    humidity_raw = 0x0000

    # Measurement data
    temperature = 0.00
    pressure = 0.00
    humidity = 0.00
