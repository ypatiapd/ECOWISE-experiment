import adc


class co2Sensor:

    def __init__(self):
        self.adc = adc.adc(0)
        self.GAIN = 1

    def get_value(self, id):
        return self.adc.get_value(id)