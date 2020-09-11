

import threading
import socket
import sys
import time
from logger import GroundLogger
import os

class ground:


    def __init__(self, elinkmanager_ip):
        """if elinkmanager_ip == 'local':
            self.uplink_host = socket.gethostname()
        else:
            self.uplink_host = '192.168.1.8'"""
        #self.uplink_host=socket.gethostname()
        self.uplink_host='192.168.1.2'  #changeeeeeeeeeeeee
        self.up_link_port=12345
        self.images_port = 12346
        self.data_port = 12347
        self.logs_port = 12348

        self.init_loggers()
        #self.info_logger=ground_logger.ground_logger('ground_info.log')
        #the buffer size
        self.BUFFER_SIZE = 1024

        #the actual logs from ground station
        #self.info_logger = logger.InfoLogger('ground.info.log')

        # bind ground to down_link_port , to receive images
        self.stop_log_threads = False
        #print(socket.gethostbyname(socket.gethostname()))
        #start threads that awaits logs
        self.start_log_threads()
        #images, Comment because moved whole image manager to new file.
        #keep it here for case of emergency
        #self.image_dir = 'GroundImages'
        #threading.Thread(target=self.open_image_connection, args=(self.images_port, )).start()


    """def connect(self):

        host="192.168.1.8"
        port=8080
        conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_socket.connect((host,port))
        while True:
            cmd = input("S: ")
            conn_socket.send(cmd.encode('utf-8'));
            if(str == "Bye" or str == "bye"):
                break
            print("N:",conn_socket.recv(1024).decode())
        conn_socket.close()"""
    def start_log_threads(self):
        """Starts log threads which will
           handle acceptance of logs
        """
        self.data_log_thread  = threading.Thread(target=self.open_connection, args=(self.data_port, ))
        self.data_log_thread.start()
        self.info_log_thread = threading.Thread(target=self.open_connection, args=(self.logs_port,))
        self.info_log_thread.start()
        #self.establish_connection()

    def init_loggers(self):

        self.data_ground_logger=GroundLogger('ground_data_logger','ground_data.log')
        self.info_ground_logger = GroundLogger('data_info_logger','data_info.log')
        self.pump_temp_logger =GroundLogger('pump_temp_logger','ground_pump_temp.log')
        self.SB_temp_logger = GroundLogger('SB_temp_logger','ground_CO2_temp.log')
        self.out_pres_logger = GroundLogger('out_pres_logger','ground_out_pres.log')
        self.out_temp_logger = GroundLogger('out_temp_logger','ground_out_temp.log')
        self.in_pres_logger = GroundLogger('in_press_logger','ground_in_pres.log')
        self.out_hum_logger = GroundLogger('out_hum_logger','ground_out_hum.log')
        self.gps_logger = GroundLogger('gps_logger','ground_gps.log')
        self.CO2_1_logger = GroundLogger('co2_1_logger','ground_CO2_1.log')
        self.CO2_2_logger = GroundLogger('co2_2_logger','ground_CO2_2.log')
        self.O3_1_logger = GroundLogger('o3_1_logger','ground_O3_1.log')
        self.O3_2_logger = GroundLogger('o3_2_logger','ground_O3_2.log')
        self.status_vector_logger=GroundLogger('status_logger','status_vector.log')
        self.stages_vector_logger=GroundLogger('stages_logger','stages_vector.log')


    def open_connection(self,port):
        """Creates a listener to {port}
           which will recieve the logs
           and will save them in Logs directory

        Arguments:
            port {string} -- The port which will bind the log listener
        """
        while True:

            #force thread to stop
            if self.stop_log_threads : break

            #host=socket.gethostname()   #changeeeeeeeeeeee
            host = '0.0.0.0'
            log_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            log_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            log_socket.bind((host, port))
            log_socket.listen(5)


            try:
                print("i am waiting")
                log_socket,addr = log_socket.accept()
                print('connected')
            except (OSError) as e:
                print("lost connection")
                #self.print_lost_connection()
                continue


            while(True):

                try:
                    data = log_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                    print("first receive="+format(data))
                except (ConnectionAbortedError, ConnectionResetError) as e:
                    #self.print_lost_connection()
                    print("lost connection1")
                    log_socket.close()
                    break


                if not data:
                    print("not data")
                    #self.info_logger.write_error('Lost connection unexpectedly from {addr} when reading filename'.format(addr=addr))
                    #print('tipotaaaaaa')
                    break

                file_name = data
                logger = self.info_ground_logger if file_name == 'info.log' else self.data_ground_logger

                try:
                    data = log_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                    print("second receive="+format(data))
                except (ConnectionAbortedError, ConnectionResetError) as e:
                    #self.print_lost_connection()
                    print("lost connection2")
                    log_socket.close()
                    break

                try:
                    total_rows = int(data)
                    #print("total_rowssss"+format(total_rows))
                except:
                    #self.info_logger.write_error('Exception on type casting for total rows. Data : {data}'.format(data=data))
                    continue

                time.sleep(0.2)

                for _ in range(total_rows):
                    try:
                        data = log_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                        print("third receive="+format(data))
                        res='Received'
                        log_socket.send(res.encode('utf-8'))
                        #self.data_logger.write_info(data)
                        #self.log_values(data)
                        time.sleep(0.2)
                    except (ConnectionResetError , ConnectionAbortedError) as e:
                        #self.info_logger.write_error('Lost connection when reading log: {log}'.format(log=data))
                        #self.print_lost_connection()
                        print("lost connection3")
                        break
        log_socket.close()

    def log_values(self,data):
        data=data
        parsed_strings = []
        measurements=[]
        stages_vector=[]
        status_vector=[]
        parsed_strings = data.split("<")
        measurements=parsed_strings[0].split('/')
        status_vector=parsed_strings[1].split('.')
        stages_vector=parsed_strings[2].split('.')
        self.SB_temp_logger.write_info(measurements[0]+measurements[1])
        self.in_pres_logger.write_info(measurements[0]+measurements[2])
        self.status_vector_logger.write_info("pump:"+status_vector[0]+"valve1:"+status_vector[1]+"valve2:"+status_vector[2]+"heater1:"+status_vector[3]+"heater2:"+status_vector[4])
        self.stages_vector_logger.write_info("stage1:"+stages_vector[0]+"stage2:"+stages_vector[1]+"stage3:"+stages_vector[2])




    def establish_connection(self):
       """Main Function to send manual commands to elinkmanager"""

       conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

       #connect to server
       while(True):
           try:
               conn_socket.connect((self.uplink_host, self.up_link_port))
               #self.info_logger.write_info("""
                # [+] Success!
                # [+] Establish Connection
                #       """)
               break
           except socket.error as e:
               print("""
                       [+] Server is Unavailabe
                       [+] or there is no internet connection.
                       [+] Try again to connect.
                       [+] Reconecting ...
                       """)
               time.sleep(2) #wait 2 seconds and retry
               continue

       #receive prompt
       prompt = conn_socket.recv(self.BUFFER_SIZE).decode('utf-8')
       #print(prompt)

       while(True):
           action = input("Action: ")
           if action == "EXIT":
               conn_socket.close()
               sys.exit(0)
           elif action =="":
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


           #save data into dictionary
           #package = {"action": action }

           #if action == "SET":
              # package['steps'] = input('Steps: ')


           #send data as json string
           try:
               conn_socket.send(action.encode('utf-8'));
               if action == "TERMINATE_EXP":
                   conn_socket.close()
                   return
               #conn_socket.sendall(json.dumps(package).encode('utf-8'))
               #get response and print it
               response = conn_socket.recv(self.BUFFER_SIZE).decode('utf-8')
               print("response="+format(response))
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
           except (TimeoutError, BrokenPipeError ) as e:
               print("""
                 [+] ElinkManager is unreachable
                 [+] Something went wrong!
                 [+] Try to reconnect...
                   """)
               break
           #print(response)


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
            #self.info_logger.write_warning('Lost internet connection.')
            #self.print_lost_connection()
            return False
