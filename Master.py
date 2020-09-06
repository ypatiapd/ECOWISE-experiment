import threading
import flow_control
#import Heat_Control
import data_handler
import elinkmanager

from logger import  InfoLogger,DataLogger

class master():

    __instance= None

    def __init__(self):
        self.ground_ip='192.168.1.1'
        self.exp_info_logger = InfoLogger('exp_info_logger', 'info.log')
        self.data_logger=DataLogger('data_logger','data.log')
        #self.data = test_data.test_data(self)
        #self.thread_data = None
        self.flow=flow_control.test_flow(self)
        self.thread_flow=None
        #self.heat=Heat_Control.HeatControl(self,info_logger)
        #self.thread_heat=None
        #self.elink = elinkmanager.ELinkManager(self,self.ground_ip)
        #self.thread_elink = None
        self.measurements = dict()
        self.commands=dict()
        self.time_measurements=dict()
        self.init_commands()
        self.measurements["Temp"] = 1111
        self.measurements["Press"] = 1000
        self.status = dict()
        self.stages=dict()
        self.init_status()


    def init_stages(self):
        self.stages["stage1"]=0
        self.stages["stage2"]=0
        self.stages["stage3"]=0


    def init_measurements(self):
        self.measurements["In_Temp"] = None
        self.measurements["Out_Temp"] = None
        self.measurements["In_Hum"] = None
        self.measurements["Out_Hum"] = None
        self.measurements["In_Press"] = 50
        self.measurements["Out_Press"] = None
        self.measurements["SB_Temp"] = None
        self.measurements["Pump_Temp"] = None
        self.measurements["Gps_X"] = None
        self.measurements["Gps_Y"] = None
        self.measurements["Gps_Time"]=None
        self.measurements["Gps_altitude"] = None
        self.measurements["CO2_1"] = None
        self.measurements["CO2_2"] = None
        self.measurements["O3_1"] = None
        self.measurements["O3_2"] = None
        self.measurements["Data_acq"]=None

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
        self.commands['OPEN_PUMP']=0
        self.commands['CLOSE_PUMP'] = 0
        self.commands['OPEN_HEAT1'] = 0
        self.commands['CLOSE_HEAT1'] = 0
        self.commands['OPEN_HEAT2'] = 0
        self.commands['CLOSE_HEAT2'] = 0
        self.commands['OPEN_VALVE1'] = 0
        self.commands['CLOSE_VALVE1'] = 0
        self.commands['OPEN_VALVE2'] = 0
        self.commands['CLOSE_VALVE2'] = 0


    def start(self):

        self.init_stages()
        self.init_measurements()
        self.init_status()
        self.init_commands()
        #self.thread_data = threading.Thread(target=self.data.read_data)
        #self.thread_data.start()
        #self.exp_info_logger.write_info("data thread is here")
        self.thread_flow = threading.Thread(target=self.flow.start_flow)
        self.thread_flow.start()
        print("flow thread is here")
        #self.thread_heat = threading.Thread(target=self.heat.heater)  # xwris parenthesi gia na min treksei i sinartisi
        #self.thread_heat.start()
        #print("heating thread is here")
        #self.thread_elink = threading.Thread(target=self.elink.start).start()
        #self.exp_info_logger.write_info("elink thread is here")
