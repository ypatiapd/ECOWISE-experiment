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
        #valve2=gpio 25
        #pump= gpio 16

        self.master=master
        self.exp_info_logger=master.exp_info_logger

        self.flow_info_logger = InfoLogger('flow_info_logger','flow_info.log')
        self.cycle_logger=InfoLogger('cycle_info_logger','cycle_info.log')
        self.pump=pump.pump(self.master)
        self.valve1=Valve.valve(1,self.master)
        self.valve2=Valve.valve(2,self.master)


    def start_flow(self):

        while 1 :
            cycle_start_time=time.time()

            cycle=self.air_cycle()
            if cycle==-1:
                self.exp_info_logger.write_info("air flow thread terminating...")
                print("air flow thread terminating...")
                return

            self.master.time_measurements['cycle']=cycle_start_time-time.time()
            self.master.time_measurements['id']=self.master.time_measurements['id']+1
            self.exp_info_logger.write_info('Cycle '+format(self.master.time_measurements['id'])+' lasted'+format(self.master.time_measurements['cycle'])+' seconds')
            #self.cycle_logger.write_info('Cycle '+format(self.master.time_measurements['id'])+' lasted'+format(self.master.time_measurements['cycle'])+' seconds')
            #self.cycle_logger.write_info('Stage1 of cycle  '+format(self.master.time_measurements['id'])+' lasted'+format(self.master.time_measurements['stage1'])+' seconds')
            #self.cycle_logger.write_info('Stage2 of cycle  '+format(self.master.time_measurements['id'])+' lasted'+format(self.master.time_measurements['stage2'])+' seconds')
            #self.cycle_logger.write_info('Stage3 of cycle  '+format(self.master.time_measurements['id'])+' lasted'+format(self.master.time_measurements['stage3'])+' seconds')

            #pws tha stelnontai katw?????mia metavliti otan teleiwnei o cycle ginetai 1 kai stelnontai mazi me ta data. san vector

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
        start_time = time.time()
        self.master.stages["stage1"]=1
        self.flow_info_logger.write_info("stage 1 begins")
        self.exp_info_logger.write_info("stage 1 begins")
        self.valve2.open_valve()
        self.master.status['valve2'] = 1
        self.valve1.open_valve()
        self.master.status['valve1'] = 1
        self.pump.ton_pump()
        self.master.status['pump'] = 1
        last_time = int(time.time())
        while (int(time.time() - last_time))< 10:  # den exei apofasistei
            cmd_state = self.check_command_vector()
            if cmd_state == 2:
                break
            elif cmd_state==4:
                self.flow_info_logger.write_info('manual cycle restart,air cycle was not completed')
                self.exp_info_logger.write_info('manual cycle restart,air cycle was not completed')
                self.master.time_measurements['stage1'] = time.time() - start_time
                return 1
            elif cmd_state==-1:
                return -1

        self.valve2.close_valve()
        self.master.status['valve2'] = 0
        print("vgika stage 1")
        self.master.stages["stage1"]=0
        self.master.time_measurements['stage1']=time.time() - start_time
        return 0


    def stage_2(self):
        print("bika stage 2")
        start_time = time.time()
        self.master.stages["stage2"]=1
        self.flow_info_logger.write_info("stage 2 begins")
        self.exp_info_logger.write_info("stage 2 begins")
        self.pump.ton_pump()
        print("i antlia anoikse")
        while self.master.measurements["In_Press"]<1000:
            print("pressure="+format(self.master.measurements["In_Press"]))
            self.master.status['pump'] = 1
            cmd_state=self.check_command_vector()
            if cmd_state == 3:
                break
            elif cmd_state==4:
                self.flow_info_logger.write_info('manual cycle restart,air cycle was not completed')
                self.exp_info_logger.write_info('manual cycle restart,air cycle was not completed')
                self.master.time_measurements['stage2'] = time.time() - start_time
                self.cycle_logger.write_info( self.master.time_measurements['stage2'])
                return 1
            elif cmd_state==-1:
                return -1

        self.flow_info_logger.write_info("presure reached in sensor box:"+format(self.master.measurements['In_Press']))
        self.valve1.close_valve()
        self.master.status['valve1'] = 0
        print("i valve1  ekleise")
        self.flow_info_logger.write_info("valve 1 closed")
        self.exp_info_logger.write_info("valve 1 closed")
        self.master.stages["stage2"]=0
        self.master.time_measurements['stage2']=time.time() - start_time
        self.cycle_logger.write_info(self.master.time_measurements['stage2'])
        return 0

    def stage_3(self):
        print("bika stage 3")
        start_time = time.time()
        self.master.stages["stage3"]=1
        self.flow_info_logger.write_info("stage 3 begins")
        self.exp_info_logger.write_info("stage 3 begins")
        last_time = int(time.time())
        print("last timeeee3"+format(last_time))
        while (int(time.time() - last_time))< 30:
            print("pressure=" + format(self.master.measurements["In_Press"]))
            #print(int(time.time() - last_time))
            cmd_state = self.check_command_vector()
            if cmd_state == 1:
                break
            elif cmd_state == 4:
                self.flow_info_logger.write_info('manual cycle restart,air cycle was not completed')
                self.exp_info_logger.write_info('manual cycle restart,air cycle was not completed')
                print('manual cycle restart,air cycle was not completed')
                self.master.time_measurements['stage3'] = time.time() - start_time
                return 1
            elif cmd_state==-1:
                return -1

        self.flow_info_logger.write_info('air cycle completed succesfully')
        self.exp_info_logger.write_info('air cycle completed succesfully')
        self.master.stages["stage3"]=0
        self.master.time_measurements['stage3']=time.time() - start_time

    def check_command_vector(self):
        if self.master.commands['STAGE_1'] == 1:
            self.flow_info_logger.write_info("Command STAGE_1 Successfuly proceeded to stage 1")
            self.exp_info_logger.write_info("Command STAGE_1 Successfuly proceeded to stage 1")
            self.master.commands['STAGE_1'] = 0
            return 1

        elif self.master.commands['STAGE_2'] == 1:
            self.flow_info_logger.write_info("Command STAGE_2 Successfuly proceeded to stage 2")
            self.exp_info_logger.write_info("Command STAGE_2 Successfuly proceeded to stage 2")
            self.master.commands['STAGE_2'] = 0
            return 2

        elif self.master.commands['STAGE_3'] == 1:
            self.flow_info_logger.write_info("Command STAGE_3 Successfuly proceeded to stage 3")
            self.flow_info_logger.write_info("Command STAGE_3 Successfuly proceeded to stage 3")
            self.master.commands['STAGE_3'] = 0
            return 3

        elif self.master.commands['NEW_CYCLE'] == 1:
            self.flow_info_logger.write_info("Command NEW_CYCLE Successfuly proceeded to new cycle")
            self.exp_info_logger.write_info("Command NEW_CYCLE Successfuly proceeded to new cycle")
            self.master.commands['NEW_CYCLE'] = 0
            return 4

        elif self.master.commands['OPEN_V1'] == 1:
            self.valve1.open_valve()
            self.flow_info_logger.write_info("Command OPEN_V1 Successfuly opened valve 1")
            self.exp_info_logger.write_info("Command OPEN_V1 Successfuly opened valve 1")
            self.master.status['valve1'] = 1
            self.master.commands['OPEN_V1'] = 0
            return 0

        elif  self.master.commands['CLOSE_V1'] == 1:
            self.valve1.close_valve()
            self.flow_info_logger.write_info("Command CLOSE_V1 Successfuly closed valve 1")
            self.exp_info_logger.write_info("Command CLOSE_V1 Successfuly closed valve 1")
            self.master.status['valve1'] = 0
            self.master.commands['CLOSE_V1'] = 0
            return 0

        elif self.master.commands['OPEN_V2'] == 1:
            self.valve2.open_valve()
            self.flow_info_logger.write_info("Command OPEN_V2 Successfuly opened valve 2")
            self.exp_info_logger.write_info("Command OPEN_V2 Successfuly opened valve 2")
            self.master.status['valve2'] = 1
            self.master.commands['OPEN_V2'] = 0
            return 0

        elif  self.master.commands['CLOSE_V2'] == 1:
            self.valve2.close_valve()
            self.flow_info_logger.write_info("Command CLOSE_V2 Successfuly closed valve 2")
            self.exp_info_logger.write_info("Command CLOSE_V2 Successfuly closed valve 2")
            self.master.status['valve2'] = 0
            self.master.commands['CLOSE_V2'] = 0
            return 0

        elif self.master.commands['TON_PUMP'] == 1:
            self.pump.ton_pump()
            self.flow_info_logger.write_info("Command TON_PUMP Successfuly turned on the pump")
            self.exp_info_logger.write_info("Command TON_PUMP Successfuly turned on the pump")
            self.master.status['pump'] = 1
            self.master.commands['TON_PUMP'] = 0
            return 0

        elif  self.master.commands['TOFF_PUMP'] == 1:
            self.pump.toff_pump()
            self.flow_info_logger.write_info("Command TOFF_PUMP Successfuly turned off the pump")
            self.exp_info_logger.write_info("Command TOFF_PUMP Successfuly turned off the pump")
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
            self.exp_info_logger.write_info("experiment terminated manually")
            self.flow_info_logger.write_info("experiment terminated manually")
            return -1
