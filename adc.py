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
        else:      # o3 adc
            self.adc= Adafruit_ADS1x15.ADS1115(address=0x4a)
        self.GAIN = 1

    def get_value(self):

        # Main loop.
        # Read all the ADC channel values in a list.
        values = [0]*4
        for i in range(4):
            # Read the specified ADC channel using the previously set gain value.
            values[i] = self.adc.read_adc(i, gain=self.GAIN)

        return values[0],values[1],values[1],values[2]
