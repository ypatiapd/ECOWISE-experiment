# /home/ypatia/bexus/heaters.py
from threading import Thread
import logging
from logger import InfoLogger
import heater
class HeatControl:

    __instance=None

    def __init__(self,master):

        self.master=master
        #self.exp_info_logger=exp_info_logger
        self.heating_info_logger=InfoLogger('heaters_info_logger','heaters.log')
        self.master=master
        self.pump_min_temp=5
        self.pump_max_temp=20
        self.sb_min_temp=-10
        self.sb_max_temp=20
        self.init_heaters()

    def turn_off_heat(self,id):
        if id==1:
            self.pump_heat.turn_off_heater(id)
            
        else:
            self.SB_heat.turn_off_heater(id)
            self.master.status["heater2"] = 0
            self.heating_info_logger.write_info("Sensor Box turned off")

    def turn_on_heat(self,id):
        if id==1:
            self.pump_heat.turn_on_heater(id)
            self.master.status["heater1"] = 1
            self.heating_info_logger.write_info("Pump heat turned on")
        else:
            self.SB_heat.turn_on_heater(id)
            self.master.status["heater2"] = 1
            self.heating_info_logger.write_info("Sensor Box heat turned on")


    def start_heating(self):

        while(1):

            self.check_heat(1, self.master.measurements['Pump_Temp'], self.master.status['heater1'])
            self.check_heat(2,self.master.measurements['In_Temp'],self.master.status['heater2'])



    def init_heaters(self):

        self.pump_heat=heater.heater(1)
        self.heating_info_logger.write_info('Pump heater instance created')
        self.SB_heat=heater.heater(2)
        self.heating_info_logger.write_info('Sensor Box heater instance created')

    def check_heat(self,id, temp, heat_on):

        if id==1:
            min_temp=self.pump_min_temp
            max_temp=self.pump_max_temp
        else :
            min_temp=self.sb_min_temp
            max_temp=self.sb_max_temp

        if temp > max_temp and heat_on:
            self.turn_off_heat(id)
        elif temp < min_temp :
            self.turn_on_heat(id)
        else:
            if id==1:
                self.heating_info_logger.write_info("Pump temperature is ok")
            else:
                self.heating_info_logger.write_info("Sensor Box temperature is ok")

