import ms5803py
from mlx90614 import MLX90614
from smbus2 import SMBus
import Adafruit_ADS1x15
from python_bme280 import bme280
import multiplexer
import CO2_sensor
import O3_sensor
import adc
from logger import InfoLogger, DataLogger
import time
import gps
import csv

class test_data:

    def __init__(self,master):
        self.master=master
        self.data_logger = master.data_logger
        self.bus = SMBus(1)
        self.init_sensors()
        self.init_loggers()
        self.init_csv()

    def init_csv(self):

        with open('data_csv.csv', 'a+', newline='') as file:
            writer = csv.writer(file)
            row = ['In_Temp', 'Out_Temp', 'In_Press', 'Out_Press', 'In_Hum', 'Out_Hum', 'Pump_Temp', 'SB_Temp', 'Gps_X',
                   'Gps_Y', 'Gps_altitude',  'O3_1_ref', 'O3_1_voltage', 'O3_2_ref', 'O3_2_voltage',
                   'CO2_1_ref', 'CO2_2_voltage', 'CO2_2_ref', 'CO2_2_voltage', 'Data_acq', 'valve_1', 'valve_2', 'heater_1', 'heater_2', 'pump', 'stage_1',
                   'stage_2', 'stage_3','cycle_id','cycle_duration','stage1_duration','stage2_duration','stage3_duration','stage1_start','stage2_start','stage3_start','Timestamp']
            writer.writerow(row)

    def init_loggers(self):

        # a logger for each measurement and one for all togeather

        self.info_logger = InfoLogger('data_info_logger','data_info.log')
        self.pump_temp_logger = DataLogger('pump_temp_logger','pump_temp.log')
        self.SB_temp_logger = DataLogger('SB_temp_logger','CO2_temp.log')
        self.out_pres_logger = DataLogger('out_pres_logger','out_pres.log')
        self.in_pres_logger = DataLogger('in_press_logger', 'in_pres.log')
        self.out_temp_logger = DataLogger('out_temp_logger','out_temp.log')
        self.in_temp_logger = DataLogger('in_temp_logger', 'in_temp.log')
        self.out_hum_logger = DataLogger('out_hum_logger','out_hum.log')
        self.in_hum_logger = DataLogger('in_hum_logger', 'in_hum.log')
        self.gps_logger = DataLogger('gps_logger','gps.log')
        self.CO2_1_logger = DataLogger('co2_1_logger','CO2_1.log')
        self.CO2_2_logger = DataLogger('co2_2_logger','CO2_2.log')
        self.O3_1_logger = DataLogger('o3_1_logger','O3_1.log')
        self.O3_2_logger = DataLogger('o3_2_logger','O3_2.log')

    def init_sensors(self):

        self.GAIN = 1
        self.multiplex = multiplexer.multiplex(1)
        self.pump_sensor = MLX90614(self.bus, address=0x12)
        self.gps = gps.gps()
        self.SB_sensor = MLX90614(self.bus, address=0x19)
        self.co2_sensor=CO2_sensor.co2Sensor()
        self.o3_sensor=O3_sensor.o3Sensor()

    def read_data(self):

        time.sleep(0.5)  # gia na prolavei na ginei i arxokopoihsh twn sensors apo master
        while 1:

            self.master.time_measurements['Timestamp']=int(round(time.time() * 1000))
            try:
                self.multiplex.channel(0x70, 4)
                self.read_Out_TH()
            except (OSError,TypeError):
                self.master.measurements["Out_Temp"] = 666
                self.master.measurements["Out_Hum"] = 666
            try:
                self.multiplex.channel(0x70, 6)
                self.read_In_TH()         # i arxikopoihsi ginetai ston multiplex des an mporei na ginei edw
            except (OSError,TypeError):
                self.master.measurements["In_Temp"] = 666
                self.master.measurements["In_Hum"] = 666
            try:
                self.multiplex.channel(0x70, 5)
                self.read_Out_Press()
            except(OSError,TypeError):
                self.master.measurements["Out_Press"] = 666
            try:
                self.multiplex.channel(0x70, 7)
                self.read_In_Press()
            except (OSError,TypeError):
                self.master.measurements["In_Press"] = 666
            try:
                self.read_Pump_Temp()  # an den trexei thelei ftiaksimo to read_object des github
            except(OSError,TypeError):
                self.master.measurements["Pump_Temp"] = 666
            try:
                self.read_SB_Temp()
            except (OSError,TypeError):
                self.master.measurements["SB_Temp"] = 666

            try:
                self.read_GPS()
            except (OSError,TypeError):
                self.master.measurements["Gps_X"]=666
                self.master.measurements["Gps_Y"]=666
                self.master.measurements["Gps_altitude"]=666
            try:
                self.read_CO2()
            except (OSError,TypeError):
                self.master.measurements["CO2_1_voltage"]=666
                self.master.measurements["CO2_1_ref"] = 666
                self.master.measurements["CO2_2_voltage"] = 666
                self.master.measurements["CO2_2_ref"] = 666
            try:
                self.read_O3()
            except (OSError,TypeError):
                self.master.measurements["O3_1_voltage"] = 666
                self.master.measurements["O3_1_ref"] = 666
                self.master.measurements["O3_2_voltage"] = 666
                self.master.measurements["O3_2_ref"] = 666

            if self.master.stages["stage3"] == 1:
                self.master.measurements["Data_acq"] = 1   #at stage 3 the sensors data are accurate
            else:
                self.master.measurements["Data_acq"] = 0
            self.log_data()
            self.log_csv()
            if self.master.commands['TERMINATE_EXP']:
                self.co2_sensor.stop_pwm()
                self.info_logger.write_info("data_handle thread terminating...")
                print("data handle thread terminating...")
                return
            time.sleep(1)   # 1 HZ sampling

    def read_Out_TH(self):

        t, p, h = self.multiplex.get_temp(4)
        t="{:.3f}".format(float(t))
        h= "{:.2f}".format(float(h))
        #print("Outside Temperature: {} °C" .format(t))
        """print("Outside Pressure: {} P".format(p))
        print("Outside Humidity: {} %%".format(h))"""
        self.master.measurements["Out_Temp"]=t
        self.master.measurements["Out_Hum"]=h

    def read_In_TH(self):

        t, p, h = self.multiplex.get_temp(6)
        t = "{:.3f}".format(float(t))
        h = "{:.2f}".format(float(t))
        #print("Inside Temperature: {} °C".format(t))
        """print("Inside Pressure: {} P".format(p))
        print("Inside Humidity: {} %%".format(h))"""
        self.master.measurements["In_Temp"] = t
        self.master.measurements["In_Hum"] = h

    def read_Out_Press(self):

        press, temp = self.multiplex.get_press(5)
        press = "{:.2f}".format(float(press))
        #print("quick'n'easy pressure={} mBar, temperature={} C".format(press, temp))
        #print(" outside pressure={} mBar".format(press))
        self.master.measurements["Out_Press"]=press

    def read_In_Press(self):

        press, temp = self.multiplex.get_press(7)
        press = "{:.2f}".format(float(press))
        #print(" inside pressure={} mBar".format(press))
        self.master.measurements["In_Press"] = press

    #oi sinartiseis den simvadizoun me tou driver tou mlx. whyyyyyyy
    def read_Pump_Temp(self):

        t = self.pump_sensor.get_ambient()
        #print("ambient temperature pump=" + format(t))
        o1 = self.pump_sensor.get_object_1()   #check mlx14 for object 1 and 2 if needs compination
        o1 = "{:.3f}".format(float(o1))
        #print("pump temperature=" + format(o1))
        o2 = self.pump_sensor.get_object_2()
        #print("object2 temperature=" + format(o2))
        self.master.measurements["Pump_Temp"] = o1

    def read_SB_Temp(self):

        t = self.SB_sensor.get_ambient()
        #print("ambient temperature SB=" + format(t))
        o1 = self.SB_sensor.get_object_1()
        o1 = "{:.3f}".format(float(o1))
        #print("SB temperature=" + format(o1))
        o2 = self.SB_sensor.get_object_2()
        #print("object2 temperature=" + format(o2))
        self.master.measurements["SB_Temp"] = o1

    def read_GPS(self):

        lat,lng,alt=self.gps.read_data2() #test me keraiaaaa
        lat= format(float(lat))
        lat = "{:.3f}".format(float(lat))
        lng = format(float(lng))
        lng = "{:.3f}".format(float(lng))
        alt = format(float(alt))
        alt = "{:.3f}".format(float(alt))
        #print("gps data"+format(lat)+",,,,,,"+format(lng))
        self.master.measurements["Gps_X"]=lat
        self.master.measurements["Gps_Y"]=lng
        self.master.measurements["Gps_altitude"]=alt

    def read_CO2(self):

        co2_1,ref_1,co2_2,ref_2=self.co2_sensor.get_value()
        #print("co2 concentration={}".format(co2))
        #print("co2 ref={}".format(ref))
        self.master.measurements["CO2_1_voltage"]=co2_1
        self.master.measurements["CO2_1_ref"] = ref_1
        self.master.measurements["CO2_2_voltage"] = co2_2
        self.master.measurements["CO2_2_ref"] = ref_2

    def read_O3(self):

        ae_2,we_2,ae_1,we_1= self.o3_sensor.get_value()
        #print("ozone_1 concentration={}".format(o3))
        #print("o3 ref={}".format(ref))
        self.master.measurements["O3_1_voltage"] = ae_2
        self.master.measurements["O3_1_ref"] = we_2
        self.master.measurements["O3_2_voltage"] =ae_1
        self.master.measurements["O3_2_ref"] = we_1

    def log_data(self):

        self.SB_temp_logger.write_info(format(self.master.measurements["SB_Temp"]))
        self.pump_temp_logger.write_info(","+format(self.master.measurements["Pump_Temp"]))
        self.in_temp_logger.write_info(","+format(self.master.measurements["In_Temp"]))
        self.out_temp_logger.write_info(","+format(self.master.measurements["Out_Temp"]))
        self.in_pres_logger.write_info(","+format(self.master.measurements["In_Press"]))
        self.out_pres_logger.write_info(","+format(self.master.measurements["Out_Press"]))
        self.in_hum_logger.write_info(","+format(self.master.measurements["In_Hum"]))
        self.out_hum_logger.write_info(","+format(self.master.measurements["Out_Hum"]))
        self.gps_logger.write_info(","+format(self.master.measurements["Gps_X"]))
        self.gps_logger.write_info(","+format(self.master.measurements["Gps_Y"]))
        self.gps_logger.write_info(","+format(self.master.measurements["Gps_altitude"]))
        # at the atmospheric sensor we log the value with the data acq variable so to know which data is accurate
        self.O3_1_logger.write_info(","+format(self.master.measurements["O3_1_ref"])+","+format(self.master.measurements["O3_1_voltage"])+","+format(self.master.measurements["Data_acq"]))
        self.O3_2_logger.write_info(","+format(self.master.measurements["O3_2_ref"])+","+format(self.master.measurements["O3_2_voltage"])+","+format(self.master.measurements["Data_acq"]))
        self.CO2_1_logger.write_info(","+format(self.master.measurements["CO2_1_ref"])+","+format(self.master.measurements["CO2_1_voltage"])+","+format(self.master.measurements["Data_acq"]))
        self.CO2_2_logger.write_info( ","+format(self.master.measurements["CO2_2_ref"])+","+format(self.master.measurements["CO2_2_voltage"])+","+format(self.master.measurements["Data_acq"]))
        self.data_logger.write_info('/'+format(self.master.measurements['In_Temp'])+'/'+format(self.master.measurements["Out_Temp"])
        +'/'+format(self.master.measurements["In_Press"])+'/'+format(self.master.measurements["Out_Press"])+'/'+format(self.master.measurements["In_Hum"])+
        '/'+format(self.master.measurements["Out_Hum"])+'/'+format(self.master.measurements["Pump_Temp"])+'/'+format(self.master.measurements["SB_Temp"])+
        '/'+format(self.master.measurements["Gps_X"])+'/'+format(self.master.measurements["Gps_Y"])+'/'+format(self.master.measurements["Gps_altitude"])+
        '/'+format(int(self.master.measurements["O3_1_ref"]))+'/'+format(self.master.measurements["O3_1_voltage"])+'/'+format(self.master.measurements["O3_2_ref"])+'/'+format(self.master.measurements["O3_2_voltage"])+'/'+format(self.master.measurements["CO2_1_ref"])
        +'/'+format(int(self.master.measurements["CO2_1_voltage"]))+'/'+format(int(self.master.measurements["CO2_2_ref"]))+'/'+format(int(self.master.measurements["CO2_2_voltage"]))+'/'+format(self.master.measurements["Data_acq"])
        +'/'+ format(self.master.time_measurements["cycle_id"])+'/'+format(self.master.time_measurements["cycle_duration"])+'/'+format(self.master.time_measurements["stage1_duration"])+'/'+format(self.master.time_measurements["stage2_duration"])+'/'+format(self.master.time_measurements["stage3_duration"])
        +'/'+format(self.master.time_measurements["stage1_start"]) +'/'+format(self.master.time_measurements["stage2_start"]) +'/'+format(self.master.time_measurements["stage3_start"])+'/'+format(self.master.time_measurements["Timestamp"])
        +'<'+format(self.master.status['valve1'])+'/'+format(self.master.status['valve2'])+'/'+
        format(self.master.status['heater1'])+'/'+format(self.master.status['heater2'])+'/'+format(self.master.status['pump'])+
        '<'+format(self.master.stages['stage1'])+"/"+format(self.master.stages['stage2'])+"/"+format(self.master.stages['stage3']))

    def log_csv(self):
        with open('data_csv.csv', 'a+', newline='') as file:
            writer = csv.writer(file)
            row=[self.master.measurements['In_Temp'],self.master.measurements["Out_Temp"],self.master.measurements["In_Press"],self.master.measurements["Out_Press"],self.master.measurements["In_Hum"],
                 self.master.measurements["Out_Hum"],self.master.measurements["Pump_Temp"],self.master.measurements["SB_Temp"],self.master.measurements["Gps_X"],self.master.measurements["Gps_Y"],
                 self.master.measurements["Gps_altitude"],self.master.measurements["O3_1_ref"],self.master.measurements["O3_1_voltage"],self.master.measurements["O3_2_ref"],self.master.measurements["O3_2_voltage"],self.master.measurements["CO2_1_ref"],
                 self.master.measurements["CO2_1_voltage"],self.master.measurements["CO2_2_ref"],self.master.measurements["CO2_2_voltage"],self.master.measurements["Data_acq"],
                 self.master.status['valve1'],self.master.status['valve2'],self.master.status['heater1'],self.master.status['heater2'],self.master.status['pump'],self.master.stages['stage1'],self.master.stages['stage2'],self.master.stages['stage3'],
                 self.master.time_measurements['cycle_id'] , self.master.time_measurements['cycle_duration'] ,self.master.time_measurements['stage1_duration'] ,self.master.time_measurements['stage2_duration'] ,self.master.time_measurements['stage3_duration'],
                 self.master.time_measurements['stage1_start'],self.master.time_measurements['stage2_start'],self.master.time_measurements['stage3_start'],self.master.time_measurements['Timestamp']]
            writer.writerow(row)



