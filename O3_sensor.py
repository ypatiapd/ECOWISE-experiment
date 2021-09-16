import adc
# to be developed
class o3Sensor:

    def __init__(self):
        self.adc =adc.adc(1)
        self.GAIN = 1

    def get_value(self):
        return self.adc.get_value()
