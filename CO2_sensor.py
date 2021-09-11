import adc
import RPi.GPIO as GPIO
#to be developed

class co2Sensor:

    def __init__(self):
        self.adc = adc.adc(0)
        self.GAIN = 1
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(19, GPIO.OUT)
        self.p1 = GPIO.PWM(19, 4)
        GPIO.setup(13, GPIO.OUT)
        self.p2 = GPIO.PWM(13, 4)
        self.p1.start(50)
        self.p2.start(50)

    def get_value(self, id):
        return self.adc.get_value(id)

    def stop_pwm(self):
        self.p1.stop()
        self.p2.stop()
