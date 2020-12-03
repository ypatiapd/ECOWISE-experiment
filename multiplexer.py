#!/usr/bin/python
import ms5803py
import smbus
from python_bme280 import bme280

class multiplex:

    def __init__(self, bus):
        self.bus = smbus.SMBus(bus)

    def channel(self, address=0x70,
                channel=0):  # values 0-3 indictae the channel, anything else (eg -1) turns off all channels

        if (channel == 0):
            action=0x01
        elif (channel == 1):
            action = 0x02
        elif (channel == 2):
            action = 0x04
        elif (channel == 3):
            action = 0x08
        elif (channel == 4):
            action = 0x10
        elif (channel == 5):
            action = 0x20
        elif (channel == 6):
            action = 0x40
        elif (channel == 7):
            action = 0x80
        else:
            action = 0x00

        self.bus.write_byte_data(address, 0x04, action)  # 0x04 is the register for switching channels
        print("channel="+format(channel))

    def get_temp(self,ch):
        bme = bme280.Bme280() # check
        bme.set_mode(bme280.MODE_FORCED)
        t, p, h = bme.get_data()
        """if (ch ==4):
            print("temperature_1=" + format(t))
        else:
            print("temperature_2="+format(t))"""
        return t, p,h


    def get_press(self,ch):

        altimeter = ms5803py.MS5803()
        press,temp=altimeter.read(pressure_osr=512)
        """if (ch == 5):
            #print("pressure_1="+format(press))
        else:
            #print("pressure_2="+format(press))"""

        return press,temp


if __name__ == '__main__':
    bus = 1  # 0 for rev1 boards etc.
    address = 0x70

    plexer = multiplex(bus)
    plexer.channel(address, 3)


    "Now run i2cdetect"