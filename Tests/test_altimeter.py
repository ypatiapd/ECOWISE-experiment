import multiplexer
import RPi.GPIO as GPIO
from logger import DataLogger
import time

logger = DataLogger('pressure_logger', 'pressure.log')

multiplex = multiplexer.multiplex(1)
GPIO.setmode(GPIO.BCM)
GPIO.setup(8,GPIO.OUT)
GPIO.output(8,GPIO.HIGH)
while 1:
    multiplex.channel(0x70, 7)
    press,temp=multiplex.get_press()
    logger.write_info(format(press))
    time.sleep(1)
    print("pressure="+format(press))
    #if press==2000:
    #    GPIO.output(8, GPIO.LOW)



