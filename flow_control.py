import RPi.GPIO as GPIO
import time
from logger import InfoLogger

class test_flow():

    __instance= None

    def __init__(self,master):

        #pins
        #valve1=gpio 7
        #valve2=gpio 25
        #pump= gpio 12

        self.master=master
        self.exp_info_logger=master.exp_info_logger
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(7,GPIO.OUT)
        GPIO.setup(25,GPIO.OUT)
        GPIO.setup(12, GPIO.OUT)
        GPIO.output(7,GPIO.LOW)
        GPIO.output(25,GPIO.LOW)
        GPIO.output(12,GPIO.LOW)

        self.flow_info_logger = InfoLogger('flow_info_logger','flow_info.log')
        self.cycle_logger=InfoLogger('cycle_info_logger','cycle_info.log')


    """def get_pressure(self):
        press,temp=self.altimeter.read(pressure_osr=512)
        return press"""


    def start_flow(self):

        while 1 :
            cycle_start_time=time.time()

            self.air_cycle()

            self.master.time_measurements['cycle']=cycle_start_time-time.time()
            self.master.time_measurements['id']+=1
            self.cycle_logger.write_info('Cycle '+format(self.master.time_measurements['id'])+' lasted'+format(self.master.time_measurements['cycle'])+' seconds')
            self.cycle_logger.write_info('Stage1 of cycle  '+format(self.master.time_measurements['id'])+' lasted'+format(self.master.time_measurements['stage1'])+' seconds')
            self.cycle_logger.write_info('Stage2 of cycle  '+format(self.master.time_measurements['id'])+' lasted'+format(self.master.time_measurements['stage2'])+' seconds')
            self.cycle_logger.write_info('Stage3 of cycle  '+format(self.master.time_measurements['id'])+' lasted'+format(self.master.time_measurements['stage3'])+' seconds')
            time.sleep(10)
            #pws tha stelnontai katw?????mia metavliti otan teleiwnei o cycle ginetai 1 kai stelnontai mazi me ta data. san vector

    def air_cycle(self):

        stage_1=self.stage_1()
        if stage_1==1:
            return
        stage_2=self.stage_2()
        if stage_2==1:
            return
        stage_3=self.stage_3()



    def stage_1(self):
        start_time = time.time()
        self.master.stages["stage1"]=1
        self.flow_info_logger.write_info("stage 1 begins")
        GPIO.output(7,GPIO.HIGH)
        self.flow_info_logger.write_info("valve 1 opened")
        self.master.status['valve1'] = 1
        GPIO.output(25,GPIO.HIGH)
        self.flow_info_logger.write_info("valve 2 opened")
        self.master.status['valve2'] = 1
        GPIO.output(12,GPIO.HIGH) #pump
        self.master.status['pump'] = 1
        self.flow_info_logger.write_info("pump is actuated")
        last_time = int(time.time())
        print("last timeeee"+format(last_time))
        while (int(time.time() - last_time))< 10:
            if self.master.commands['STAGE_2']==1:
                self.flow_info_logger.write_info('proceed to stage 2 manually')
                self.master.commands['STAGE_2']=0
                break
            if self.master.commands['NEW_CYCLE']==1:
                self.flow_info_logger.write_info('proceed from stage 1 to new cycle manually')
                self.master.commands['NEW_CYCLE']=0
                self.flow_info_logger.write_info('manual cycle restart,air cycle was not completed')
                self.master.time_measurements['stage1']=time.time() - start_time
                return 1
        GPIO.output(25,GPIO.LOW)
        self.master.status['valve2'] = 0
        self.flow_info_logger.write_info("valve 2 closed")
        self.master.stages["stage1"]=0
        self.master.time_measurements['stage1']=time.time() - start_time


    def stage_2(self):

        start_time = time.time()
        self.master.stages["stage2"]=1
        self.flow_info_logger.write_info("stage 2 begins")
        self.flow_info_logger.write_info("pump is filling the sensor box with air......")
        GPIO.output(12,GPIO.HIGH)
        self.master.measurements["Press"]=1014
        while self.master.measurements["Press"]<1013:
            self.master.status['pump'] = 1
            if self.master.commands['STAGE_3']==1:
                self.flow_info_logger.write_info('proceed to stage 3 manually')
                self.master.commands['STAGE_3']=0
                break
            if self.master.commands['NEW_CYCLE']==1:
                self.flow_info_logger.write_info('proceed from stage 2 to new cycle manually')
                self.master.commands['NEW_CYCLE']=0
                self.flow_info_logger.write_info('manual cycle restart,air cycle was not completed')
                self.master.time_measurements['stage2']=time.time() - start_time
                return 1

            #print("pump is sucking air"+format(self.master.measurements["Press"]))
        #GPIO.output(7,GPIO.LOW)
        self.master.status['pump'] = 0
        self.flow_info_logger.write_info("pump turned off")
        self.flow_info_logger.write_info("presure reached in sensor box:"+format(self.master.measurements['Press']))
        #GPIO.output(24, GPIO.LOW)
        self.master.status['valve1'] = 0
        self.flow_info_logger.write_info("valve 1 closed")
        self.master.stages["stage2"]=0
        self.master.time_measurements['stage2']=time.time() - start_time

    def stage_3(self):

        start_time = time.time()
        self.master.stages["stage3"]=1
        self.flow_info_logger.write_info("stage 3 begins")
        self.flow_info_logger.write_info("data acquisition..........")
        last_time = int(time.time())
        print("last timeeee"+format(last_time))
        while (int(time.time() - last_time))< 30:
            #print(format(time.time() - last_time)+"timeeeeeee")
            if self.master.commands['STAGE_1']==1:
                self.flow_info_logger.write_info('proceed to stage 1 manually')
                self.master.commands['STAGE_1']=0
                break
            if self.master.commands['NEW_CYCLE']==1:
                self.flow_info_logger.write_info('proceed from stage 3 to new cycle manually')
                self.master.commands['NEW_CYCLE']=0
                self.master.time_measurements['stage3']=time.time() - start_time
                self.flow_info_logger.write_info('manual cycle restart,air cycle was not completed')
                return 1
        self.flow_info_logger.write_info('air cycle completed succesfully')
        #total time of air cycle DOOOOO
        self.master.stages["stage3"]=0
        self.master.time_measurements['stage3']=time.time() - start_time
