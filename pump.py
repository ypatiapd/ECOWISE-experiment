import RPi.GPIO as GPIO



class pump:

    def __init__(self,master):
        self.master=master
        self.pump_pin=16
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pump_pin, GPIO.OUT)
        GPIO.output(self.pump_pin, GPIO.LOW)
        self.exp_info_logger = self.master.exp_info_logger
        self.exp_info_logger.write_info("pump instance created")

    def ton_pump(self):

        GPIO.output(self.pump_pin, GPIO.HIGH)
        self.exp_info_logger.write_info("pump turned on")
        self.master.status['pump'] = 1

    def toff_pump(self):

        GPIO.output(self.pump_pin, GPIO.LOW)
        self.exp_info_logger.write_info("pump turned off")
        self.master.status['pump'] = 0
