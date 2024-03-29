import RPi.GPIO as GPIO


class valve:

    def __init__(self, valve_number,master):
        self.master=master
        self.valve_number = valve_number
        self.solenoid_pin = None
        if self.valve_number == 1:
            self.solenoid_pin = 8
        elif self.valve_number == 2:
            self.solenoid_pin = 7
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.solenoid_pin, GPIO.OUT)
        GPIO.output(self.solenoid_pin, GPIO.LOW)

    def open_valve(self):
        GPIO.output(self.solenoid_pin, GPIO.HIGH)

    def close_valve(self):
        GPIO.output(self.solenoid_pin, GPIO.LOW)



