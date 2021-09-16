import RPi.GPIO as GPIO

class pump:

    def __init__(self,master):
        self.master=master
        self.pump_pin=16
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pump_pin, GPIO.OUT)
        GPIO.output(self.pump_pin, GPIO.LOW)

    def ton_pump(self):
        state = GPIO.input(self.pump_pin)
        if not state:
            GPIO.output(self.pump_pin, GPIO.HIGH)
        self.master.status['pump'] = 1

    def toff_pump(self):

        GPIO.output(self.pump_pin, GPIO.LOW)
        self.master.status['pump'] = 0
