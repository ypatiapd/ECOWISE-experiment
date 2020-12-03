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



# calibration proceedure just in case needed
"""while True:
                # Read all the ADC channel values in a list.
                values = [0] * 4
                for i in range(4):
                    # Read the specified ADC channel using the previously set gain value.
                    values[i] = self.adc.read_adc(i, gain=self.GAIN)
                    values[i] = values[i] * 1.724 / 13785

                # Note you can also pass in an optional data_rate parameter that controls
                # the ADC conversion time (in samples/second). Each chip has a different
                # set of allowed data rate values, see datasheet Table 9 config register
                # DR bit values.
                # values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
                # Each value will be a 12 or 16 bit signed integer value depending on the
                # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
                # Print the ADC values.

                # R=100.2*(values[2]-values[3])/(3.3-(values[2]-values[3]))
                # temp_anal=(R-101)/0.385
                # temp_anal = (333.3 - 201.2 * (values[2] - values[3])) / (0.385 * (values[2] - values[3]) - 1.2705)

                temp_anal = 355.522 * values[3] - 608.232
                print("temp_analllll=" + format(temp_anal))
                print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
                # Pause for half a second.
                # temp = temp_sensor.get_ambient()
                # print("tempMLX="+format(temp))"""