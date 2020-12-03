import RPi.GPIO as GPIO


class valve:

    def __init__(self, valve_number,master):
        self.master=master
        self.valve_number = valve_number
        self.solenoid_pin = None
        if self.valve_number == 1:
            self.solenoid_pin = 8
        elif self.valve_number == 2:
            #self.solenoid_pin = 25
            self.solenoid_pin = 7
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.solenoid_pin, GPIO.OUT)
        GPIO.output(self.solenoid_pin, GPIO.LOW)
        self.exp_info_logger = self.master.exp_info_logger
        self.exp_info_logger.write_info("valve" + format(self.valve_number) + "created")

    def open_valve(self):

        GPIO.output(self.solenoid_pin, GPIO.HIGH)
        self.exp_info_logger.write_info("valve" + format(self.valve_number) + "opened")


    def close_valve(self):

        GPIO.output(self.solenoid_pin, GPIO.LOW)
        self.exp_info_logger.write_info("valve" + format(self.valve_number) + "closed")


