#!/usr/bin/python
import smbus
from datetime import datetime
import dateutil.parser

class RealTimeClock:
    def __init__(self):
        pass

    def Update(self):
        self.GetRegisterData()
        self.UpdateTimestamp()

    def GetTimestamp(self):
        return self.timestamp

    def SetTimeFromSystemClock(self):
        self.SetTimeFromTimestamp(datetime.utcnow().isoformat())

    def SetTimeFromTimestamp(self, timestamp):
        dt = dateutil.parser.parse(timestamp).replace(tzinfo=None, microsecond=0)
        self.year = dt.year
        self.month = dt.month
        self.day = dt.isoweekday()
        self.date = dt.day
        self.hour = dt.hour
        self.minute = dt.minute
        self.second = dt.second
        self.hour_mode = 0
        self.am_pm = 0

        self.register_data[0] = (self.second % 10) + (((self.second - (self.second % 10))/10) << 4)
        self.register_data[1] = (self.minute % 10) + (((self.minute - (self.minute % 10))/10) << 4)
        self.register_data[2] = (self.hour % 10) | (((self.hour - (self.hour % 10))/10) << 4) | (self.hour_mode<<6) | (self.am_pm<<5)
        self.register_data[3] = self.day
        self.register_data[4] = (self.date % 10) + (((self.date - (self.date % 10))/10) << 4)
        self.register_data[5] = (self.month % 10) + (((self.month - (self.month % 10))/10) << 4)
        self.register_data[6] = (self.year % 10) + ((((self.year % 100) - (self.year % 10))/10) << 4)

        self.SetRegisterData()

    # Low level functions
    def GetRegisterData(self):
        bus = smbus.SMBus(1)
        for n in range(0, 16):
            self.register_data[n] = bus.read_byte_data(0x68, n)
        bus.close()

    def SetRegisterData(self):
        bus = smbus.SMBus(1)
        
        # Write only first 15 registers, 16th is a status read-only register
        for n in range(0, 15):
            self.register_data[n] = bus.write_byte_data(0x68, n, self.register_data[n])
        bus.close()

    def UpdateTimestamp(self):
        self.second = (self.register_data[0] >> 4)*10 + (self.register_data[0] & 0b1111)
        self.minute = (self.register_data[1] >> 4)*10 + (self.register_data[1] & 0b1111)
        self.hour_mode = (self.register_data[2] >> 6) & 0x01

        # 24 hour mode
        if self.hour_mode == 0:
            self.hour = ((self.register_data[2] >> 4) & 0b11)*10 + (self.register_data[2] & 0b1111)

        # 12 hour mode
        elif self.hour_mode == 1:
            self.hour = ((self.register_data[2] >> 4) & 0x01)*10 + (self.register_data[2] & 0b1111)
            self.am_pm = (self.register_data[2] >> 5) & 0x01

        self.day = self.register_data[3]
        self.date = (self.register_data[4] >> 4)*10 + (self.register_data[4] & 0b1111)
        self.month = (((self.register_data[5] >> 4) & 0x01)*10 + (self.register_data[5] & 0b1111))
        self.century = self.register_data[5] >> 7
        self.year = 2000 + ((self.register_data[6] >> 4)*10 + (self.register_data[6] & 0b1111))

        self.timestamp = datetime(year=self.year, month=self.month, day=self.date, hour=self.hour, minute=self.minute, second=self.second).isoformat() + 'Z'

    # Register level data
    register_data = [ 0x00 ] * 16

    # Timestamp data
    second = 0
    minute = 0
    hour = 0
    am_pm = 0
    hour_mode = 0 # 0 -> 12 hour mode, 1 -> 24 hour mode
    day = 0
    date = 0
    month = 0
    century = 0 # This bit triggers if the year register overflows from 99 to 0
    year = 0

    timestamp = ""
