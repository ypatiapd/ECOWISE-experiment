import Rpi.GPIO as GPIO

class heater:

      def __init__(self,id):

            self.id=id
            if id==1:
                  GPIO.setup(17,GPIO.OUT)
                  GPIO.output(17,GPIO.LOW)
            else :
                  GPIO.setup(18,GPIO.OUT)
                  GPIO.output(18,GPIO.LOW)

      def turn_on_heater(self,id):
            if id==1:
                  GPIO.output(17,GPIO.HIGH)
            else :
                  GPIO.output(18,GPIO.HIGH)

      def turn_off_heater(self,id):
            if id==1:
                  GPIO.output(17,GPIO.LOW)
            else :
                  GPIO.output(18,GPIO.LOW)
