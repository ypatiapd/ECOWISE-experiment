import adc

# This class is going to be filled with calibration algorithms

class o3Sensor:

    def __init__(self):
        self.adc =adc.adc(1)
        self.GAIN = 1

    def get_value(self,id):
        return self.adc.get_value(id)
