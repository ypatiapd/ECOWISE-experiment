import RPi.GPIO as GPIO


class valve:

    def __init__(self):
        self.solenoid_pin = None
        self.solenoid_pin = 8
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.solenoid_pin, GPIO.OUT)
        GPIO.output(self.solenoid_pin, GPIO.LOW)

    def open_valve(self):

        GPIO.output(self.solenoid_pin, GPIO.HIGH)


    def close_valve(self):

        GPIO.output(self.solenoid_pin, GPIO.LOW)



