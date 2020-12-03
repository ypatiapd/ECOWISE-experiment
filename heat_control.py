# /home/ypatia/bexus/heaters.py
from threading import Thread
import logging
from logger import InfoLogger
import heater
class HeatControl:

    __instance=None

    def __init__(self,master):

        self.master=master
        self.exp_info_logger=master.exp_info_logger
        self.heating_info_logger=InfoLogger('heaters_info_logger','heaters.log')
        self.master=master
        self.pump_min_temp=5
        self.pump_max_temp=20
        self.sb_min_temp=15
        self.sb_max_temp=20
        self.init_heaters()

    def turn_off_heat(self,id):
        if id==1:
            self.pump_heat.turn_off_heater(id)
            self.master.status["heater1"] = 0
            self.heating_info_logger.write_info("Pump heater turned off")
            self.exp_info_logger.write_info("Pump heater turned off")
            
        else:
            self.SB_heat.turn_off_heater(id)
            self.master.status["heater2"] = 0
            self.heating_info_logger.write_info("Sensor Box heater turned off")
            self.exp_info_logger.write_info("Sensor Box heater turned off")

    def turn_on_heat(self,id):
        if id==1:
            self.pump_heat.turn_on_heater(id)
            self.master.status["heater1"] = 1
            self.heating_info_logger.write_info("Pump heat turned on")
            self.exp_info_logger.write_info("Pump heater turned on")
        else:
            self.SB_heat.turn_on_heater(id)
            self.master.status["heater2"] = 1
            self.heating_info_logger.write_info("Sensor Box heat turned on")
            self.exp_info_logger.write_info("Sensor Box heater turned on")


    def start_heating(self):

        while(1):

            a=self.check_heat(1, self.master.measurements['Pump_Temp'], self.master.status['heater1'])
            b=self.check_heat(2,self.master.measurements['SB_Temp'],self.master.status['heater2'])
            if a or b == -1 :
                print("bika")
                return




    def init_heaters(self):

        self.pump_heat=heater.heater(1)
        self.heating_info_logger.write_info('Pump heater instance created')
        self.exp_info_logger.write_info("Pump heater instance created")
        self.SB_heat=heater.heater(2)
        self.heating_info_logger.write_info('Sensor Box heater instance created')
        self.exp_info_logger.write_info("Sensor Box heater instance created")

    def check_heat(self,id, temp, heat_on):

        if self.master.commands['TERMINATE_EXP']:
            self.exp_info_logger.write_info("heat control thread terminating...")
            print("heat control thread terminating...")
            return -1

        self.check_command_vector()

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

    def check_command_vector(self):

        if self.master.commands['TON_H1'] == 1:
            self.turn_on_heat(1)
            self.heating_info_logger.write_info("Command TON_H1 Successfuly turned on  Pump heater ")
            self.exp_info_logger.write_info("Command TON_H1 Successfuly turned on Pump heater")
            self.master.status['heater1'] = 1
            self.master.commands['TON_H1'] = 0
            return 0

        elif self.master.commands['TOFF_H1'] == 1:
            self.turn_off_heat(1)
            self.heating_info_logger.write_info("Command TOFF_H1 Successfuly turned off Pump heater")
            self.exp_info_logger.write_info("Command TOFF_H1 Successfuly turned off Pump heater")
            self.master.status['heater1'] = 0
            self.master.commands['TOFF_H1'] = 0
            return 0

        elif self.master.commands['TON_H2'] == 1:
            self.turn_on_heat(2)
            self.heating_info_logger.write_info("Command TON_H2 Successfuly turned on SB heater ")
            self.exp_info_logger.write_info("Command TON_H2 Successfuly turned on SB heater")
            self.master.status['heater2'] = 1
            self.master.commands['TON_H2'] = 0
            return 0

        elif self.master.commands['TOFF_H2'] == 1:
            self.turn_off_heat(2)
            self.heating_info_logger.write_info("Command TOFF_H2 Successfuly turned off SB heater ")
            self.exp_info_logger.write_info("Command TOFF_H2 Successfuly turned off SB heater ")
            self.master.status['heater2'] = 0
            self.master.commands['TOFF_H2'] = 0
            return 0



