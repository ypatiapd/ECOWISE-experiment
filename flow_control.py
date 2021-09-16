import RPi.GPIO as GPIO
import time
from logger import InfoLogger
import Valve
import pump

class flowControl():

    __instance= None

    def __init__(self,master):

        #pins
        #valve1=gpio 8
        #valve2=gpio 7
        #pump= gpio 16

        self.master=master
        self.flow_info_logger = InfoLogger('flow_info_logger','flow_info.log')
        self.cycle_logger=InfoLogger('cycle_info_logger','cycle_info.log')
        self.pump=pump.pump(self.master)
        self.valve1=Valve.valve(1,self.master)
        self.valve2=Valve.valve(2,self.master)

    def start_flow(self):

        while 1 :
            cycle_start_time=int(round(time.time() * 1000))
            cycle=self.air_cycle()
            if cycle==-1:
                self.flow_info_logger.write_info("air flow thread terminating...")
                print("air flow thread terminating...")
                return
            self.master.time_measurements['cycle_duration']=int(round(time.time() * 1000))-cycle_start_time
            self.master.time_measurements['cycle_id']=format(int(self.master.time_measurements['cycle_id'])+1)

    def air_cycle(self):
        stage_1=self.stage_1()
        if stage_1==1:
            return 1
        elif stage_1==-1:
            return -1
        stage_2=self.stage_2()
        if stage_2==1:
            return 1
        elif stage_2==-1:
            return -1
        stage_3=self.stage_3()
        if stage_3==-1:
            return -1

    def stage_1(self):
        print("bika stage 1")
        start_time = int(round(time.time() * 1000))
        self.master.time_measurements['stage1_start']=start_time
        self.master.stages["stage1"]=1
        self.valve2.open_valve()
        self.master.status['valve2'] = 1
        self.valve1.open_valve()
        self.master.status['valve1'] = 1
        self.pump.ton_pump()
        self.master.status['pump'] = 1
        last_time = int(round(time.time() * 1000))
        while (int(int(round(time.time() * 1000)) - last_time))< 10000:  # den exei apofasistei
            cmd_state = self.check_command_vector()
            if cmd_state == 2:
                break
            elif cmd_state==4:
                self.flow_info_logger.write_info('manual cycle restart,air cycle was not completed')
                self.master.time_measurements['stage1_duration'] = int(round(time.time() * 1000)) - start_time
                return 1
            elif cmd_state==-1:
                return -1
            time.sleep(1) # gia na min trwei cpu

        self.valve2.close_valve()
        self.master.status['valve2'] = 0
        print("vgika stage 1")
        self.master.stages["stage1"]=0
        self.master.time_measurements['stage1_duration']=int(round(time.time() * 1000)) - start_time
        return 0

    def stage_2(self):
        print("bika stage 2")
        start_time = int(round(time.time() * 1000))
        self.master.time_measurements['stage2_start'] = start_time
        self.master.stages["stage2"]=1
        self.pump.ton_pump()
        self.master.status['pump'] = 1
        while float(self.master.measurements["In_Press"])<1000.00:
            #print("pressure="+format(self.master.measurements["In_Press"]))
            if (int((int(round(time.time() * 1000)) - start_time))> 300000) and (float(self.master.measurements["In_Press"])>800.00):
                break
            cmd_state=self.check_command_vector()
            if cmd_state == 3:
                break
            elif cmd_state==4:
                self.flow_info_logger.write_info('manual cycle restart,air cycle was not completed')
                self.master.time_measurements['stage2_duration'] = int(round(time.time() * 1000)) - start_time
                self.cycle_logger.write_info( self.master.time_measurements['stage2_duration'])
                return 1
            elif cmd_state==-1:
                return -1
            time.sleep(1)# gia na min trwei cpu

        self.flow_info_logger.write_info("presure reached in sensor box:"+format(self.master.measurements['In_Press']))
        self.valve1.close_valve()
        self.master.status['valve1'] = 0
        print("i valve1  ekleise")
        self.master.stages["stage2"]=0
        self.master.time_measurements['stage2_duration']=int(round(time.time() * 1000)) - start_time
        self.cycle_logger.write_info(self.master.time_measurements['stage2_duration'])
        return 0

    def stage_3(self):
        print("bika stage 3")
        start_time = int(round(time.time() * 1000))
        self.master.time_measurements['stage3_start'] = start_time
        self.master.stages["stage3"]=1
        self.pump.ton_pump()
        self.master.status['pump'] = 1
        last_time = int(round(time.time() * 1000))
        while (int(int(round(time.time() * 1000)) - last_time))< 30000:
            #print("pressure_stage3=" + format(self.master.measurements["In_Press"]))
            #print(int(time.time() - last_time))
            cmd_state = self.check_command_vector()
            if cmd_state == 1:
                break
            elif cmd_state == 4:
                self.flow_info_logger.write_info('manual cycle restart,air cycle was not completed')
                print('manual cycle restart,air cycle was not completed')
                self.master.time_measurements['stage3_duration'] = int(round(time.time() * 1000)) - start_time
                return 1
            elif cmd_state==-1:
                return -1
            time.sleep(1)# gia na min trwei cpu

        self.master.stages["stage3"]=0
        self.master.time_measurements['stage3_duration']=int(round(time.time() * 1000)) - start_time

    def check_command_vector(self):
        if self.master.commands['STAGE_1'] == 1:
            self.flow_info_logger.write_info("Command STAGE_1 Successfuly proceeded to stage 1")
            self.master.commands['STAGE_1'] = 0
            return 1

        elif self.master.commands['STAGE_2'] == 1:
            self.flow_info_logger.write_info("Command STAGE_2 Successfuly proceeded to stage 2")
            self.master.commands['STAGE_2'] = 0
            return 2

        elif self.master.commands['STAGE_3'] == 1:
            self.flow_info_logger.write_info("Command STAGE_3 Successfuly proceeded to stage 3")
            self.master.commands['STAGE_3'] = 0
            return 3

        elif self.master.commands['NEW_CYCLE'] == 1:
            self.flow_info_logger.write_info("Command NEW_CYCLE Successfuly proceeded to new cycle")
            self.master.commands['NEW_CYCLE'] = 0
            return 4

        elif self.master.commands['OPEN_V1'] == 1:
            self.valve1.open_valve()
            self.flow_info_logger.write_info("Command OPEN_V1 Successfuly opened valve 1")
            self.master.status['valve1'] = 1
            self.master.commands['OPEN_V1'] = 0
            return 0

        elif  self.master.commands['CLOSE_V1'] == 1:
            self.valve1.close_valve()
            self.flow_info_logger.write_info("Command CLOSE_V1 Successfuly closed valve 1")
            self.master.status['valve1'] = 0
            self.master.commands['CLOSE_V1'] = 0
            return 0

        elif self.master.commands['OPEN_V2'] == 1:
            self.valve2.open_valve()
            self.flow_info_logger.write_info("Command OPEN_V2 Successfuly opened valve 2")
            self.master.status['valve2'] = 1
            self.master.commands['OPEN_V2'] = 0
            return 0

        elif  self.master.commands['CLOSE_V2'] == 1:
            self.valve2.close_valve()
            self.flow_info_logger.write_info("Command CLOSE_V2 Successfuly closed valve 2")
            self.master.status['valve2'] = 0
            self.master.commands['CLOSE_V2'] = 0
            return 0

        elif self.master.commands['TON_PUMP'] == 1:
            self.pump.ton_pump()
            self.flow_info_logger.write_info("Command TON_PUMP Successfuly turned on the pump")
            self.master.status['pump'] = 1
            self.master.commands['TON_PUMP'] = 0
            return 0

        elif  self.master.commands['TOFF_PUMP'] == 1:
            self.pump.toff_pump()
            self.flow_info_logger.write_info("Command TOFF_PUMP Successfuly turned off the pump")
            self.master.status['pump'] = 0
            self.master.commands['TOFF_PUMP'] = 0
            return 0

        elif self.master.commands['TERMINATE_EXP']==1:

            self.valve1.close_valve()
            self.master.status['valve1'] = 1
            self.valve2.close_valve()
            self.master.status['valve2'] = 1
            self.pump.toff_pump()
            self.master.status['pump'] = 0
            self.flow_info_logger.write_info("experiment terminated manually")
            return -1
