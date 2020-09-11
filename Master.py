import threading
import flow_control
import heat_control
import data_handler
import elinkmanager
import time

from logger import  InfoLogger,DataLogger

class master():

    __instance= None

    def __init__(self):
        self.ground_ip='192.168.1.1'
        self.exp_info_logger = InfoLogger('exp_info_logger', 'info.log')
        self.data_logger=DataLogger('data_logger','data.log')
        self.data = data_handler.test_data(self)
        self.thread_data = None
        self.flow=flow_control.flowControl(self)
        self.thread_flow=None
        self.heat=heat_control.HeatControl(self)
        self.thread_heat=None
        self.elink = elinkmanager.ELinkManager(self,self.ground_ip)
        self.thread_elink = None
        self.measurements = dict()
        self.commands=dict()
        self.time_measurements=dict()
        self.init_commands()
        self.status = dict()
        self.stages=dict()
        self.init_status()


    def init_stages(self):
        self.stages["stage1"]=0
        self.stages["stage2"]=0
        self.stages["stage3"]=0


    def init_measurements(self):
        self.measurements["In_Temp"] = 0
        self.measurements["Out_Temp"] = 0
        self.measurements["In_Hum"] = 0
        self.measurements["Out_Hum"] = 0
        self.measurements["In_Press"] = 0
        self.measurements["Out_Press"] = 0
        self.measurements["SB_Temp"] = 0
        self.measurements["Pump_Temp"] = 0
        self.measurements["Gps_X"] = 0
        self.measurements["Gps_Y"] = 0
        self.measurements["Gps_Time"]=0
        self.measurements["Gps_altitude"] = 0
        self.measurements["CO2_1"] = 0
        self.measurements["CO2_2"] = 0
        self.measurements["O3_1"] = 0
        self.measurements["O3_2"] = 0
        self.measurements["Data_acq"]=0

    def init_status(self):
        self.status['valve1'] = 0
        self.status['valve2'] = 0
        self.status['heater1'] = 0
        self.status['heater2'] = 0
        self.status['pump'] = 0

    def init_time_measurements(self):
        self.time_measurements['stage1']=0
        self.time_measurements['stage2']=0
        self.time_measurements['stage3']=0
        self.time_measurements['cycle']=0
        self.time_measurements['id']=0

    def init_commands(self):
        self.commands['STAGE_1']=0
        self.commands['STAGE_2']=0
        self.commands['STAGE_3']=0
        self.commands['NEW_CYCLE']=0
        self.commands['RESTART_EXP']=0
        self.commands['TERMINATE_EXP']=0
        self.commands['RESTART_LOGS']=0
        self.commands['TON_PUMP']=0
        self.commands['TOFF_PUMP'] = 0
        self.commands['TON_H1'] = 0
        self.commands['TOFF_H1'] = 0
        self.commands['TON_H2'] = 0
        self.commands['TOFF_H2'] = 0
        self.commands['OPEN_V1'] = 0
        self.commands['CLOSE_V1'] = 0
        self.commands['OPEN_V2'] = 0
        self.commands['CLOSE_V2'] = 0
        self.commands['TERMINATE_EXP']=0


    def start(self):

        self.init_stages()
        self.init_measurements()
        self.init_status()
        self.init_commands()
        self.thread_data = threading.Thread(target=self.data.read_data)
        self.thread_data.start()
        self.exp_info_logger.write_info("data thread is here")
        self.thread_flow = threading.Thread(target=self.flow.start_flow)
        self.thread_flow.start()
        self.exp_info_logger.write_info("flow thread is here")
        self.thread_heat = threading.Thread(target=self.heat.start_heating)  # xwris parenthesi gia na min treksei i sinartisi
        self.thread_heat.start()
        self.exp_info_logger.write_info("heating thread is here")
        self.thread_elink = threading.Thread(target=self.elink.start).start()
        self.exp_info_logger.write_info("elink thread is here")
        while not self.commands['TERMINATE_EXP'] :
            time.sleep(5)
        time.sleep(5)
        return