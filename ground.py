import threading
import socket
import sys
import time
from logger import GroundLogger
import os
import time
import matplotlib.animation as animation
import datetime
from collections import deque
import csv

class ground:
    # by default define the interval as being 1000 mSec
    intervalAnim = 800

    def __init__(self, elinkmanager_ip):
        """if elinkmanager_ip == 'local':
            self.uplink_host = socket.gethostname()
        else:
            self.uplink_host = '192.168.1.8'"""
        # self.uplink_host=socket.gethostname()  # in case 1 pc
        self.uplink_host = '192.168.1.23'  # changeeeeeeeeeeeee
        self.up_link_port = 12345
        self.images_port = 12346
        self.data_port = 12347
        self.logs_port = 12348

        self.init_loggers()

        self.BUFFER_SIZE = 1024

        # the actual logs from ground station

        # bind ground to down_link_port , to receive images
        self.stop_log_threads = False
        # start threads that awaits logs

        self.command = ""
        self.data = dict()
        self.status = dict()
        self.stages = dict()
        self.init_data()
        self.init_status()
        self.init_stages()
        self.init_csv()
        self.start_log_threads()


    # vectors to store acquired data from the experiment
    # the stage vector includes the states of the stages (0/1)
    def init_csv(self):

        with open('data_csv.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            row = ['Timestamp','In_Temp', 'Out_Temp', 'In_Press', 'Out_Press', 'In_Hum', 'Out_Hum', 'Pump_Temp', 'SB_Temp', 'Gps_X',
                   'Gps_Y', 'Gps_altitude', 'O3_1_ref', 'O3_1_voltage', 'O3_2_ref', 'O3_2_voltage',
                   'CO2_1_ref', 'CO2_2_voltage', 'CO2_2_ref', 'CO2_2_voltage', 'Data_acq', 'valve_1', 'valve_2', 'heater_1', 'heater_2', 'pump', 'stage_1',
                   'stage_2', 'stage_3','cycle_id','cycle_duration','stage1_duration','stage2_duration','stage3_duration','stage1_start','stage2_start','stage3_start']
            writer.writerow(row)

    def init_stages(self):
        self.stages["stage1"] = 0
        self.stages["stage2"] = 0
        self.stages["stage3"] = 0

    # the status vector includes the following components of the experiment (0/1)
    def init_status(self):
        self.status['valve1'] = 0
        self.status['valve2'] = 0
        self.status['heater1'] = 0
        self.status['heater2'] = 0
        self.status['pump'] = 0

    # the data vector includes the measurements of the sensors
    def init_data(self):
        self.data["Timestamp"]=0
        self.data["In_Temp"] = 0
        self.data["Out_Temp"] = 0
        self.data["In_Hum"] = 0
        self.data["Out_Hum"] = 0
        self.data["In_Press"] = 0
        self.data["Out_Press"] = 0
        self.data["SB_Temp"] = 0
        self.data["Pump_Temp"] = 0
        self.data["Gps_X"] = 0
        self.data["Gps_Y"] = 0
        self.data["Gps_altitude"] = 0
        self.data["CO2_1_ref"] = 0
        self.data["CO2_1_voltage"] = 0
        self.data["CO2_2_ref"] = 0
        self.data["CO2_2_voltage"] = 0
        self.data["O3_1_ref"] = 0
        self.data["O3_1_voltage"] = 0
        self.data["O3_2_ref"] = 0
        self.data["O3_2_voltage"] = 0
        self.data["Data_acq"] = 0
        self.data["cycle_id"] = 0
        self.data["cycle_duration"] = 0
        self.data["stage1_duration"] = 0
        self.data["stage2_duration"] = 0
        self.data["stage3_duration"] = 0
        self.data["stage1_start"] = 0
        self.data["stage2_start"] = 0
        self.data["stage3_start"] = 0

    def start_log_threads(self):
        """Starts log threads which will
           handle acceptance of logs
        """
        self.data_log_thread = threading.Thread(target=self.open_connection, args=(self.data_port,))
        self.data_log_thread.start()
        # self.info_log_thread = threading.Thread(target=self.open_connection, args=(self.logs_port,))
        # self.info_log_thread.start()

    def init_loggers(self):

        self.data_ground_logger = GroundLogger('ground_data_logger', 'ground_data.log')
        self.info_ground_logger = GroundLogger('data_info_logger', 'ground_info.log')
        self.pump_temp_logger = GroundLogger('pump_temp_logger', 'ground_pump_temp.log')
        self.SB_temp_logger = GroundLogger('SB_temp_logger', 'ground_CO2_temp.log')
        self.out_pres_logger = GroundLogger('out_pres_logger', 'ground_out_pres.log')
        self.in_temp_logger = GroundLogger('in_temp_logger', 'ground_in_temp.log')
        self.out_temp_logger = GroundLogger('out_temp_logger', 'ground_out_temp.log')
        self.in_pres_logger = GroundLogger('in_press_logger', 'ground_in_pres.log')
        self.in_hum_logger = GroundLogger('in_hum_logger', 'ground_in_hum.log')
        self.out_hum_logger = GroundLogger('out_hum_logger', 'ground_out_hum.log')
        self.gps_logger = GroundLogger('gps_logger', 'ground_gps.log')
        self.CO2_1_logger = GroundLogger('co2_1_logger', 'ground_CO2_1.log')
        self.CO2_2_logger = GroundLogger('co2_2_logger', 'ground_CO2_2.log')
        self.O3_1_logger = GroundLogger('o3_1_logger', 'ground_O3_1.log')
        self.O3_2_logger = GroundLogger('o3_2_logger', 'ground_O3_2.log')
        self.status_vector_logger = GroundLogger('status_logger', 'status_vector.log')
        self.stages_vector_logger = GroundLogger('stages_logger', 'stages_vector.log')

    def open_connection(self, port):
        """Creates a listener to {port}
           which will recieve the logs
           and will save them in Logs directory

        Arguments:
            port {string} -- The port which will bind the log listener
        """
        while True:

            # force thread to stop
            if self.stop_log_threads: break

            # host=socket.gethostname()   #if there is one pc
            host = '0.0.0.0'
            log_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            log_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            log_socket.bind((host, port))
            log_socket.listen(5)

            try:
                #print("i am waiting")
                log_socket, addr = log_socket.accept()
                #print('connected')
            except (OSError) as e:
                print("lost connection")
                continue

            while (True):

                try:
                    data = log_socket.recv(self.BUFFER_SIZE).decode(
                        'utf-8')  # the name of the file that the data were sended (data or info)
                    print("first receive=" + format(data))
                except (ConnectionAbortedError, ConnectionResetError) as e:
                    print("lost connection1")
                    log_socket.close()
                    break

                if not data:
                    #print("not data")
                    # self.info_logger.write_error('Lost connection unexpectedly from {addr} when reading filename'.format(addr=addr))
                    break

                file_name = data
                logger = self.info_ground_logger if file_name == 'info.log' else self.data_ground_logger

                try:
                    data = log_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                    print("second receive=" + format(data))
                except (ConnectionAbortedError, ConnectionResetError) as e:
                    print("lost connection2")
                    log_socket.close()
                    break

                try:
                    total_rows = int(data)  # total rows of sended data file
                except:
                    # self.info_logger.write_error('Exception on type casting for total rows. Data : {data}'.format(data=data))
                    continue

                time.sleep(0.2)

                for _ in range(total_rows):
                    try:
                        data = log_socket.recv(self.BUFFER_SIZE).decode('utf-8')  # the sended data
                        print("third receive=" + format(data))
                        res = 'Received'
                        log_socket.sendall(res.encode('utf-8'))
                        logger.write_info(data)
                        if file_name == "data.log":  # store in different files each measurement for safety and visualisation
                            self.log_values(data)
                            time.sleep(0.2)
                    except (ConnectionResetError, ConnectionAbortedError) as e:
                        # self.info_logger.write_error('Lost connection when reading log: {log}'.format(log=data))
                        # self.print_lost_connection()
                        print("lost connection3")
                        break
        log_socket.close()

    def log_values(self, data):
        data = data
        parsed_strings = []
        measurements = []
        stages_vector = []
        status_vector = []
        parsed_strings = data.split("<")
        measurements = parsed_strings[0].split('/')
        status_vector = parsed_strings[1].split('/')
        stages_vector = parsed_strings[2].split('/')

        self.stages["stage1"] = stages_vector[0]
        self.stages["stage2"] = stages_vector[1]
        self.stages["stage3"] = stages_vector[2]

        self.status['valve1'] = status_vector[0]
        self.status['valve2'] = status_vector[1]
        self.status['heater1'] = status_vector[2]
        self.status['heater2'] = status_vector[3]
        self.status['pump'] = status_vector[4]

        self.data['In_Temp'] = measurements[1]
        self.data['Out_Temp'] = measurements[2]
        self.data['In_Press'] = measurements[3]
        self.data['Out_Press'] = measurements[4]
        print("OUT_PRESSURE" + format(self.data['Out_Press']))
        self.data['In_Hum'] = measurements[5]
        self.data['Out_Hum'] = measurements[6]
        self.data['Pump_Temp'] = measurements[7]
        self.data['SB_Temp'] = measurements[8]
        self.data['Gps_X'] = measurements[9]
        self.data['Gps_Y'] = measurements[10]
        self.data['Gps_altitude'] = measurements[11]
        self.data['O3_1_ref'] = measurements[12]
        self.data['O3_1_voltage'] = measurements[13]
        self.data['O3_2_ref'] = measurements[14]
        self.data['O3_2_voltage'] = measurements[15]
        self.data['CO2_1_ref'] = measurements[16]
        self.data['CO2_1_voltage'] = measurements[17]
        self.data['CO2_2_ref'] = measurements[18]
        self.data['CO2_2_voltage'] = measurements[19]
        self.data["Data_acq"] = measurements[20]
        self.data["cycle_id"] = measurements[21]
        self.data["cycle_duration"] = measurements[22]
        self.data["stage1_duration"] = measurements[23]
        self.data["stage2_duration"] = measurements[24]
        self.data["stage3_duration"] = measurements[25]
        self.data["stage1_start"] = measurements[26]
        self.data["stage2_start"] = measurements[27]
        self.data["stage3_start"] = measurements[28]
        self.data['Timestamp'] = measurements[29]

        self.in_temp_logger.write_info(measurements[0] +","+ measurements[1])
        self.out_temp_logger.write_info(measurements[0] +","+ measurements[2])
        self.in_pres_logger.write_info(measurements[0] +","+ measurements[3])
        self.out_pres_logger.write_info(measurements[0] +","+ measurements[4])
        self.in_hum_logger.write_info(measurements[0] +","+ measurements[5])
        self.out_hum_logger.write_info(measurements[0] +","+ measurements[6])
        self.pump_temp_logger.write_info(measurements[0] +","+ measurements[7])
        self.SB_temp_logger.write_info(measurements[0] +","+ measurements[8])
        self.gps_logger.write_info(measurements[0] +","+ measurements[9] + "," + measurements[10] + "," + measurements[11])
        # at the gas sensors we also put the data acq variable to know at which stage we took the measurements
        self.O3_1_logger.write_info(measurements[0] +","+ measurements[12] + "," + measurements[13]+ "," + measurements[20])
        self.O3_2_logger.write_info(measurements[0] +","+ measurements[14] + "," + measurements[15]+ "," + measurements[20])
        self.CO2_1_logger.write_info(measurements[0] +","+ measurements[16] + "," + measurements[17]+ "," + measurements[20])
        self.CO2_2_logger.write_info(measurements[0] +","+ measurements[18] + "," + measurements[19]+ "," + measurements[20])
        self.status_vector_logger.write_info(
            measurements[0] +","+ status_vector[0] + "," + status_vector[1] + "," + status_vector[2] + "," + status_vector[
                3] + "," + status_vector[4])
        self.stages_vector_logger.write_info(
            measurements[0] +","+ stages_vector[0] + "," + stages_vector[1] + "," + stages_vector[2])

        with open('data_csv.csv', 'a+', newline='') as file:
            writer = csv.writer(file)
            row=[self.data['In_Temp'],self.data["Out_Temp"],self.data["In_Press"],self.data["Out_Press"],self.data["In_Hum"],
                 self.data["Out_Hum"],self.data["Pump_Temp"],self.data["SB_Temp"],self.data["Gps_X"],self.data["Gps_Y"],
                 self.data["Gps_altitude"],self.data["O3_1_ref"],self.data["O3_1_voltage"],self.data["O3_2_ref"],self.data["O3_2_voltage"],self.data["CO2_1_ref"],
                 self.data["CO2_1_voltage"],self.data["CO2_2_ref"],self.data["CO2_2_voltage"],self.data["Data_acq"],
                 self.data['cycle_id'], self.data['cycle_duration'],
                 self.data['stage1_duration'], self.data['stage2_duration'],
                 self.data['stage3_duration'],
                 self.data['stage1_start'], self.data['stage2_start'],
                 self.data['stage3_start'],self.data['Timestamp'],
                 self.status['valve1'],self.status['valve2'],self.status['heater1'],self.status['heater2'],self.status['pump'],self.stages['stage1'],self.stages['stage2'],self.stages['stage3']]
            writer.writerow(row)


    def establish_connection(self):
        """Main Function to send manual commands to elinkmanager"""

        conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to server
        while (True):
            try:
                conn_socket.connect((self.uplink_host, self.up_link_port))
                self.info_ground_logger.write_info("""
                 [+] Success!
                 [+] Establish Connection
                      """)
                print("ground:connected")
                break
            except socket.error as e:
                print("""
                       [+] Server is Unavailabe
                       [+] or there is no internet connection.
                       [+] Try again to connect.
                       [+] Reconecting ...
                       """)
                time.sleep(2)  # wait 2 seconds and retry
                continue

        # receive prompt
        prompt = conn_socket.recv(self.BUFFER_SIZE).decode('utf-8')

        while (True):
            action = self.command
            # print("action ="+format(action))
            if action == "EXIT":
                conn_socket.close()
                sys.exit(0)
            elif action == "":
                continue
            """elif action == "RESTART_GROUND_LOGS":
                self.stop_log_threads = True
                if self.data_log_thread.isAlive():
                    self.data_log_thread.join()
                if self.info_log_thread.isAlive():
                    self.info_log_thread.join()
                self.stop_log_threads = False
                self.start_log_threads()
                continue"""
            # save data into dictionary
            # package = {"action": action }

            # if action == "SET":
            # package['steps'] = input('Steps: ')

            # send data as json string
            try:
                conn_socket.sendall(action.encode('utf-8'))
                """if action == "TERMINATE_EXP":
                    conn_socket.close()
                    return"""
                # conn_socket.sendall(json.dumps(package).encode('utf-8')) # des to auto ti kanei
                # get response and print it
                response = conn_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                print("response=" + format(response))
                self.command = ""  # clear the command variable

            except ConnectionAbortedError as e:
                print("""
                   [+] Lost Connection.
                   [+] Unable to send action {action}.
                   [+] Initialize connection.
                   [+] Please wait....
                   """.format(action=action))
                break
            except ConnectionResetError as e:
                print("""
                 [+] Unable to send action {action}.
                 [+] Initialize connection.
                 [+] Please wait....
                   """.format(action=action))
                break
            except (TimeoutError, BrokenPipeError) as e:
                print("""
                 [+] ElinkManager is unreachable
                 [+] Something went wrong!
                 [+] Try to reconnect...
                   """)
                break
            # print(response)

    def print_lost_connection(self):
        """Print warning about internet
           Connection
        """
        print("""
                  [+] Lost Internet Connection
                  [+] Trying to reconnect...
             """)

    def has_internet_connection(self):
        """
            Function to check internet connection.
        """
        try:
            _ = requests.get('http://www.google.com/', timeout=5)
            return True
        except:
            # self.info_logger.write_warning('Lost internet connection.')
            # self.print_lost_connection()
            return False

    def send_command(self, args):
        self.command = args

    def nt(self, fig):

        self.xs = deque([] * 20, maxlen=20)
        self.ys = deque([] * 20, maxlen=20)
        self.ys1 = deque([] * 20, maxlen=20)
        # self.ys2 = deque([] * 30, maxlen=30)
        # self.ys3 = deque([] * 30, maxlen=30)

        self.ax = fig.add_subplot(1, 1, 1)
        self.ax.set_title("Pressure over time")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Pressure")

        # create empty plot at start
        self.line, = self.ax.plot([], [], color="black")
        self.line1, = self.ax.plot([], [], color="orange")
        # self.line2, = self.ax.plot([], [], color="green")
        # self.line3, = self.ax.plot([], [], color="black")

        self.anim = animation.FuncAnimation(fig, self.animate, interval=self.intervalAnim, repeat=True,
                                            cache_frame_data=False)

    def animate(self, i):

        self.ys.append(float(self.data['In_Press']))
        self.xs.append(datetime.datetime.now())
        self.ys1.append(float(self.data['Out_Press']))
        # self.ys2.append(self.data['SB_Temp'] )
        # self.ys3.append(self.data["Pump_Temp"])

        # update data in existing plot
        self.line.set_data(self.xs, self.ys)
        self.line1.set_data(self.xs, self.ys1)
        # self.line2.set_data(self.xs, self.ys2)
        # self.line3.set_data(self.xs, self.ys3)

        self.ax.relim()
        self.ax.set_autoscale_on(True)
        self.ax.autoscale_view(True, True, True)
