import time
#from mlx90614 import MLX90614
from smbus2 import SMBus
import RPi.GPIO as GPIO
# Import the ADS1x15 module.
import Adafruit_ADS1x15


class adc:

    def __init__(self, sensor_type):

        self.bus = SMBus(1)
        if sensor_type==0:   # co2 adc
            self.adc = Adafruit_ADS1x15.ADS1115(address=0x48)
            self.a=431 / 3470000
            self.b=12063/173500
        else:      # o3 adc
            self.adc= Adafruit_ADS1x15.ADS1115(address=0x4a)
            self.a=171 / 1379000
            self.b=16679/275800
        self.GAIN = 1

    def get_value(self):

        # Main loop.
        # Read all the ADC channel values in a list.
        values = [0]*4
        volt = [0] * 4
        for i in range(4):
            # Read the specified ADC channel using the previously set gain value.
            values[i] = self.adc.read_adc(i, gain=self.GAIN)
            volt[i] = (self.a) * values[i] + self.b

        return volt[0],volt[1],volt[1],volt[2]


#Ο3:::volt[i] = (171 / 1379000) * values[i] + 16679/275800
#co2:::volt[i] = (431 / 3470000) * values[i] + 12063/173500
