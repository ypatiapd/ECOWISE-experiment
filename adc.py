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
            self.setup_adc()   # co2 sensor needs pwm
        else:      # o3 adc
            self.adc= Adafruit_ADS1x15.ADS1115(address=0x4a)
        self.GAIN = 1


    def setup_adc(self):

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(13, GPIO.OUT)
        p = GPIO.PWM(13, 4)
        p.start(50)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(19, GPIO.OUT)
        p = GPIO.PWM(19, 4)
        p.start(50)


    def get_value(self,id):

        """print('Reading ADS1x15 values, press Ctrl-C to quit...')
        # Print nice channel column headers.
        print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
        print('-' * 37)"""
        # Main loop.
        # Read all the ADC channel values in a list.
        values = [0]*4
        for i in range(4):
            # Read the specified ADC channel using the previously set gain value.
            values[i] = self.adc.read_adc(i, gain=self.GAIN)

        #print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
        if id==1:
            return values[0],values[1]
        else:
            return values[1],values[2]
        #time.sleep(0.5)



