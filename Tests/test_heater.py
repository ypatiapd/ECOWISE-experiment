import RPi.GPIO as GPIO
#from mlx90614 import MLX90614
#from smbus2 import SMBus
from logger import InfoLogger

class test_heater:

        def __init__(self,master):
            self.master=master
            self.info_logger = InfoLogger('heat_info_logger','heat_info.log')
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(17, GPIO.OUT)

        """def get_obj_temp(self):
            return self.temp_sensor.get_obj_temp()"""

        def heater(self):

            while 1:

                if self.master.measurements["Temp"] < 10:
                    GPIO.output(17,GPIO.HIGH)
                else:
                    GPIO.output(17,GPIO.LOW)

            return

