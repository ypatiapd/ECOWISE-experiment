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

class test_data:

    def __init__(self,master):
        self.master=master
        self.exp_info_logger=master.exp_info_logger
        self.data_logger = master.data_logger
        self.bus = SMBus(1)
        self.init_sensors()
        self.init_loggers()


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

        #the initializations of the multiplexer sensors happen inside the multiplexer
        """self.bme_out = bme280.Bme280()
        #self.bme_out.set_mode(bme280.MODE_FORCED)
        #self.bme_in = bme280.Bme280()
        #self.bme_in.set_mode(bme280.MODE_FORCED)
        
        #self.alt_in= ms5803py.MS5803()"""
        #self.alt_out = ms5803py.MS5803(address=0x76)
        time.sleep(1)

        self.multiplex = multiplexer.multiplex(1)
        self.pump_sensor = MLX90614(self.bus, address=0x12)
        #self.gps = gps.gps()
        self.SB_sensor = MLX90614(self.bus, address=0x19)
        self.co2_sensor=CO2_sensor.co2Sensor()
        self.o3_sensor=O3_sensor.o3Sensor()
        self.co2_adc=adc.adc(0)
        self.o3_adc=adc.adc(1)  #initialize with adc channel
        self.exp_info_logger.write_info("sensors initialized")


    def read_data(self):
        time.sleep(0.5)  # gia na prolavei na ginei i arxokopoihsh twn sensors apo master
        while 1:
            # kapoies fores vgazei error tsekare an paizei kati me bus kai i2c

            #self.multiplex.channel(0x70, 4)
            #self.read_Out_TH()
            self.multiplex.channel(0x70, 6)
            self.read_In_TH()         # i arxikopoihsi ginetai ston multiplex des an mporei na ginei edw
            #self.multiplex.channel(0x70, 5)
            #self.read_Out_Press()
            self.multiplex.channel(0x70, 7)
            self.read_In_Press()
            #press, temp = self.alt_out.read(pressure_osr=512) # GIA TO TEEEEEEEEEEEEEEEEEEEEEST
            self.read_Pump_Temp()  # an den trexei thelei ftiaksimo to read_object des github
            self.read_SB_Temp()
            #self.read_GPS()    # thelei ftiaksimo to read_data()
            self.read_CO2_1()
            self.read_CO2_2()
            self.read_O3_1()
            self.read_O3_2()
            if self.master.stages["stage3"] == 1:
                self.master.measurements["Data_acq"] = 1   #at stage 3 the sensors data are accurate
            else:
                self.master.measurements["Data_acq"] = 0
            self.log_data()

            if self.master.commands['TERMINATE_EXP']:
                self.exp_info_logger.write_info("data_handle thread terminating...")
                print("data handle thread terminating...")
                return
            time.sleep(1)   # 1 HZ sampling

    def read_Out_TH(self):

        t, p, h = self.multiplex.get_temp(4)

        """print("Outside Temperature: {} °C" .format(t))
        print("Outside Pressure: {} P".format(p))
        print("Outside Humidity: {} %%".format(h))"""
        self.master.measurements["Out_Temp"]=t
        self.master.measurements["Out_Hum"]=h

    def read_In_TH(self):

        t, p, h = self.multiplex.get_temp(6)

        """print("Inside Temperature: {} °C".format(t))
        print("Inside Pressure: {} P".format(p))
        print("Inside Humidity: {} %%".format(h))"""
        self.master.measurements["In_Temp"] = t
        self.master.measurements["In_Hum"] = h


    def read_Out_Press(self):

        press, temp = self.multiplex.get_press(5)

        #print("quick'n'easy pressure={} mBar, temperature={} C".format(press, temp))
        """raw_temperature = self.alt_out.read_raw_temperature(osr=4096)
        raw_pressure = self.alt_out.read_raw_pressure(osr=4096)
        press, temp = self.alt_out.convert_raw_readings(raw_pressure, raw_temperature)
        print(" outside pressure={} mBar, outside temperature={} C".format(press, temp))"""
        self.master.measurements["Out_Press"]=press



    def read_In_Press(self):

        press, temp = self.multiplex.get_press(7)

        """print("quick'n'easy pressure={} mBar, temperature={} C".format(press, temp))"""
        """raw_temperature = self.alt_in.read_raw_temperature(osr=4096)
        raw_pressure = self.alt_in.read_raw_pressure(osr=4096)
        press, temp = self.alt_in.convert_raw_readings(raw_pressure, raw_temperature)
        print(" inside pressure={} mBar, inside temperature={} C".format(press, temp))"""
        self.master.measurements["In_Press"] = press

    #oi sinartiseis den simvadizoun me tou driver tou mlx. whyyyyyyy
    def read_Pump_Temp(self):

        t = self.pump_sensor.get_ambient()
        #print("ambient temperature pump=" + format(t))
        o1 = self.pump_sensor.get_object_1()   #check mlx14 for object 1 and 2 if needs compination
        #print("pump temperature=" + format(o1))
        #o2 = self.pump_sensor.get_object_2()
        #print("object2 temperature=" + format(o2))
        self.master.measurements["Pump_Temp"] = o1

    def read_SB_Temp(self):

        t = self.SB_sensor.get_ambient()
        #print("ambient temperature SB=" + format(t))
        o1 = self.SB_sensor.get_object_1()
        #print("SB temperature=" + format(o1))
        o2 = self.SB_sensor.get_object_2()
        #print("object2 temperature=" + format(o2))
        SB_temp = 20
        self.master.measurements["SB_Temp"] = o1

    def read_GPS(self):

        data=self.gps.read_data2() #test me keraiaaaa
        #print(data)
        #self.master.measurements["Gps_X"]=lattitude
        #self.master.measurements["Gps_Y"]=longtitude
        #self.master.measurements["Gps_Time"]=altitude

    def read_CO2_1(self):

        co2,ref=self.co2_sensor.get_value(1)
        #print("co2 concentration={}".format(co2))
        self.master.measurements["CO2_1"]=co2

    def read_CO2_2(self):

        co2,ref = self.co2_sensor.get_value(2)
        #print("co2 concentration={}".format(co2))
        self.master.measurements["CO2_2"] = co2


    def read_O3_1(self):

        o3,ref= self.o3_sensor.get_value(1)
        #print("ozone_1 concentration={}".format(o3))
        self.master.measurements["O3_1"] = o3


    def read_O3_2(self):

        o3,ref = self.o3_sensor.get_value(2)
        #print("ozone_2 concentration={}".format(o3))
        self.master.measurements["O3_2"] = o3

    def log_data(self):

        self.SB_temp_logger.write_info(","+format(self.master.measurements["SB_Temp"]))
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
        self.O3_1_logger.write_info(","+format(self.master.measurements["O3_1"])+","+format(self.master.measurements["Data_acq"]))
        self.O3_2_logger.write_info(","+format(self.master.measurements["O3_2"])+","+format(self.master.measurements["Data_acq"]))
        self.CO2_1_logger.write_info(","+format(self.master.measurements["CO2_1"])+","+format(self.master.measurements["Data_acq"]))
        self.CO2_2_logger.write_info( ","+format(self.master.measurements["CO2_2"])+","+format(self.master.measurements["Data_acq"]))
        #self.data_logger.write_info("Data acquisition: " + format(self.master.measurements["Data_acq"]))
        self.data_logger.write_info(',/'+format(int(self.master.measurements['In_Temp']))+'/'+format(int(self.master.measurements["Out_Temp"]))
        +'/'+format(int(self.master.measurements["In_Press"]))+'/'+format(int(self.master.measurements["Out_Press"]))+'/'+format(int(self.master.measurements["In_Hum"]))+
        '/'+format(int(self.master.measurements["Out_Hum"]))+'/'+format(int(self.master.measurements["Pump_Temp"]))+'/'+format(int(self.master.measurements["SB_Temp"]))+
        '/'+format(self.master.measurements["Gps_X"])+'/'+format(self.master.measurements["Gps_Y"])+'/'+format(self.master.measurements["Gps_altitude"])+
        '/'+format(int(self.master.measurements["O3_1"]))+'/'+format(int(self.master.measurements["O3_2"]))+'/'+format(int(self.master.measurements["CO2_1"]))+'/'+format(int(self.master.measurements["CO2_2"]))+'/'+format(self.master.measurements["Data_acq"])
        +'<'+format(self.master.status['valve1'])+'/'+format(self.master.status['valve2'])+'/'+
        format(self.master.status['heater1'])+'/'+format(self.master.status['heater2'])+'/'+format(self.master.status['pump'])+
        '<'+format(self.master.stages['stage1'])+"/"+format(self.master.stages['stage2'])+"/"+format(self.master.stages['stage3']))
        self.info_logger.write_info('all data logged')
