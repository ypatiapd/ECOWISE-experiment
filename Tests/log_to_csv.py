import csv
from file_read_backwards import FileReadBackwards

with open('thermal.csv', 'a+', newline='') as file:
    writer = csv.writer(file)
    row = ['Timestamp', 'In_Temp', 'Out_Temp', 'In_Press', 'Out_Press', 'In_Hum', 'Out_Hum', 'Pump_Temp', 'SB_Temp',
           'Gps_X',
           'Gps_Y', 'Gps_altitude', 'O3_1_ref', 'O3_1_voltage', 'O3_2_ref', 'O3_2_voltage',
           'CO2_1_ref', 'CO2_2_voltage', 'CO2_2_ref', 'CO2_2_voltage', 'Data_acq', 'cycle_id',
           'cycle_duration', 'stage1_duration', 'stage2_duration', 'stage3_duration',
           'stage1_start', 'stage2_start', 'stage3_start', 'valve_1', 'valve_2', 'heater_1', 'heater_2', 'pump',
           'stage_1', 'stage_2', 'stage_3']
    writer.writerow(row)


with FileReadBackwards('C:/Users/ypatia/Desktop/software_bexus/thermal_test.txt', encoding="utf-8") as log_file:
    for line in log_file:
        parsed_strings = line.split("<")
        measurements = parsed_strings[0].split('/')
        status_vector = parsed_strings[1].split('/')
        stages_vector = parsed_strings[2].split('/')

        stage1 = stages_vector[0]
        stage2 = stages_vector[1]
        stage3 = stages_vector[2]

        valve1 = status_vector[0]
        valve2 = status_vector[1]
        heater1 = status_vector[2]
        heater2 = status_vector[3]
        pump = status_vector[4]

        In_Temp = (float(measurements[1]))
        Out_Temp = (float(measurements[2]))
        In_Press = (float(measurements[3]))
        Out_Press = (float(measurements[4]))
        In_Hum = int(float(measurements[5]))
        Out_Hum = int(float(measurements[6]))
        Pump_Temp = (float(measurements[7]))
        SB_Temp = (float(measurements[8]))
        Gps_X = (float(measurements[9]))
        Gps_Y = (float(measurements[10]))
        Gps_altitude = (float(measurements[11]))
        O3_1_ref = measurements[12]
        O3_1_voltage = measurements[13]
        O3_2_ref = measurements[14]
        O3_2_voltage = measurements[15]
        CO2_1_ref = measurements[16]
        CO2_1_voltage = measurements[17]
        CO2_2_ref = measurements[18]
        CO2_2_voltage = measurements[19]
        Data_acq = measurements[20]
        cycle_id = measurements[21]
        cycle_duration = measurements[22]
        stage1_duration = measurements[23]
        stage2_duration = measurements[24]
        stage3_duration = measurements[25]
        stage1_start = measurements[26]
        stage2_start= measurements[27]
        stage3_start = measurements[28]
        Timestamp = measurements[29]

        with open('thermal.csv', 'a+', newline='') as file:
            writer = csv.writer(file)
            row=[Timestamp,In_Temp,Out_Temp,In_Press,Out_Press,In_Hum,
                 Out_Hum,Pump_Temp,SB_Temp,Gps_X,Gps_Y,
                 Gps_altitude,O3_1_ref,O3_1_voltage,O3_2_ref,O3_2_voltage,CO2_1_ref,
                 CO2_1_voltage,CO2_2_ref,CO2_2_voltage,Data_acq,
                 cycle_id, cycle_duration,stage1_duration, stage2_duration,stage3_duration,
                 stage1_start, stage2_start,stage3_start,
                 valve1,valve2,heater1,heater2,pump,stage1,stage2,stage3]
            writer.writerow(row)


