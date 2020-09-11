import RPi.GPIO as GPIO

class heater:

      def __init__(self,id):
            GPIO.setmode(GPIO.BCM)
            self.id=id
            if id==1:
                  GPIO.setup(16,GPIO.OUT)
                  GPIO.output(16,GPIO.LOW)
            else :
                  GPIO.setup(17,GPIO.OUT)
                  GPIO.output(17,GPIO.LOW)

      def turn_on_heater(self,id):
            if id==1:
                  GPIO.output(16,GPIO.HIGH)
            else :
                  GPIO.output(17,GPIO.HIGH)

      def turn_off_heater(self,id):
            if id==1:
                  GPIO.output(16,GPIO.LOW)
            else :
                  GPIO.output(17,GPIO.LOW)
