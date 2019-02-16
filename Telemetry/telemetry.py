#!/usr/bin/python
import rtc
import environment
import imu
import adc

class TelemetryManager:
    def __init__(self):
        pass

    # High level functions
    def Update(self):
        self.UpdateSubModules()
        #print self.analog_to_digital_converter.GetVoltages()
        self.WriteDataPacketToFile('/home/pi/Desktop/telemetry_data.csv')

    # Low level functions
    def UpdateSubModules(self):
        self.real_time_clock.Update()
        self.environment_sensor.Update()
        self.inertial_measurement_unit.Update()
        self.analog_to_digital_converter.Update()

        self.telemetry_data = []
        self.telemetry_data.append(self.real_time_clock.GetTimestamp())
        self.telemetry_data.append(str(self.environment_sensor.GetTemperature()))
        self.telemetry_data.append(str(self.environment_sensor.GetPressure()))
        self.telemetry_data.append(str(self.environment_sensor.GetHumidity()))

        accel = self.inertial_measurement_unit.GetAcceleration()
        self.telemetry_data.append(str(accel[0]))
        self.telemetry_data.append(str(accel[1]))
        self.telemetry_data.append(str(accel[2]))

        gyro = self.inertial_measurement_unit.GetGyrometer()
        self.telemetry_data.append(str(gyro[0]))
        self.telemetry_data.append(str(gyro[1]))
        self.telemetry_data.append(str(gyro[2]))

        mag = self.inertial_measurement_unit.GetMagnetometer()
        self.telemetry_data.append(str(mag[0]))
        self.telemetry_data.append(str(mag[1]))
        self.telemetry_data.append(str(mag[2]))

        voltages = self.analog_to_digital_converter.GetVoltages()
        for n in range(0, len(voltages)):
            self.telemetry_data.append(str(voltages[n]))

    def WriteDataPacketToFile(self, filename):
        handle = open(filename, "a")
        for n in range(0, len(self.telemetry_data)):
            handle.write(self.telemetry_data[n])
            if n == len(self.telemetry_data)-1:
                handle.write('\n')

            else:
                handle.write(',')

        handle.close()

    # Telemetry sub-modules
    real_time_clock = rtc.RealTimeClock()
    environment_sensor = environment.EnvironmentSensor()
    inertial_measurement_unit = imu.InertialMeasurementUnit()
    analog_to_digital_converter = adc.AnalogToDigitalConverter()

    # Telemetry data packet
    telemetry_data = []
