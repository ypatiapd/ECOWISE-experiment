import time
#from mlx90614 import MLX90614
from smbus2 import SMBus
import RPi.GPIO as GPIO
# Import the ADS1x15 module.
import Adafruit_ADS1x15

bus = SMBus(1)
adc = Adafruit_ADS1x15.ADS1115(address=0x48)
GAIN = 1

values = [0]*4
volt = [0]*4

while(True):
    for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        values[i] = adc.read_adc(i, gain=GAIN)
        volt[i] = (433/3467000)* values[i] +(74/86675)
    print("-----" + format(volt[0]) + "------" + format(volt[1]) + "------" + format(volt[2]) + "-------" + format(volt[3]))
    #print("-----" + format(values[0]) + "------" + format(values[1]) + "------" + format(values[2]) + "-------" + format(values[3]))


#o3_new:::volt[i] =  (433/3467000) * values[i] - (74/86675)
#co2:::volt[i] = (431 / 3470000) * values[i] + 12063/173500
