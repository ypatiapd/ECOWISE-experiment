import RPi.GPIO as GPIO

class pump_for_test:

    def __init__(self):
        self.pump_pin=16
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pump_pin, GPIO.OUT)
        GPIO.output(self.pump_pin, GPIO.LOW)

    def ton_pump(self):

        GPIO.output(self.pump_pin, GPIO.HIGH)

    def toff_pump(self):

        GPIO.output(self.pump_pin, GPIO.LOW)
