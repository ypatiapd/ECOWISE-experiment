# /home/ypatia/bexus/heaters.py
from threading import Thread
import logging
from logger import InfoLogger
import heater
import time
class HeatControl:

    __instance=None

    def __init__(self,master):

        self.master=master
        self.heating_info_logger=InfoLogger('heaters_info_logger','heaters.log')
        self.pump_min_temp=5.00
        self.pump_max_temp=25.00
        self.sb_min_temp=5.00
        self.sb_max_temp=25.00
        self.init_heaters()

    def turn_off_heat(self,id):
        if id==1:
            self.pump_heat.turn_off_heater(id)
            self.master.status["heater1"] = 0
            
        else:
            self.SB_heat.turn_off_heater(id)
            self.master.status["heater2"] = 0

    def turn_on_heat(self,id):
        if id==1:
            self.pump_heat.turn_on_heater(id)
            self.master.status["heater1"] = 1

        else:
            self.SB_heat.turn_on_heater(id)
            self.master.status["heater2"] = 1

    def start_heating(self):
        a=0
        b=0
        while(1):
            self.check_command_vector()
            if self.master.commands['TON_H1'] != 1:
                a=self.check_heat(1, self.master.measurements['Pump_Temp'], self.master.status['heater1'])
            if self.master.commands['TON_H2'] != 1:
                b=self.check_heat(2,self.master.measurements['SB_Temp'],self.master.status['heater2'])
            if a or b == -1 :
                return
            time.sleep(5)# gia na min trwei cpu

    def init_heaters(self):

        self.pump_heat=heater.heater(1)
        self.heating_info_logger.write_info('Pump heater instance created')
        self.SB_heat=heater.heater(2)
        self.heating_info_logger.write_info('Sensor Box heater instance created')

    def check_heat(self,id, temp, heat_on):

        if self.master.commands['TERMINATE_EXP']:
            self.heating_info_logger.write_info("heat control thread terminating...")
            return -1

        if id==1:
            min_temp=self.pump_min_temp
            max_temp=self.pump_max_temp
        else :
            min_temp=self.sb_min_temp
            max_temp=self.sb_max_temp

        if float(temp) > max_temp and heat_on:
            self.turn_off_heat(id)
        elif float(temp) < min_temp :
            self.turn_on_heat(id)

    def check_command_vector(self):
        if self.master.commands['TON_H1'] == 1:
            self.turn_on_heat(1)
            self.master.status['heater1'] = 1
            if self.master.commands['TOFF_H1'] == 1:
                self.turn_off_heat(1)
                self.master.status['heater1'] = 0
                self.master.commands['TOFF_H1'] = 0
                self.master.commands['TON_H1'] = 0
        if self.master.commands['TON_H2'] == 1:
            self.turn_on_heat(2)
            self.master.status['heater2'] = 1
            if self.master.commands['TOFF_H2'] == 1:
                self.turn_off_heat(2)
                self.master.status['heater2'] = 0
                self.master.commands['TOFF_H2'] = 0
                self.master.commands['TON_H2'] = 0
            return 0



