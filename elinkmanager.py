# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 01:22:57 2020

@author: vayos
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 00:16:33 2020

@author: vayos
"""

import socket
import threading
import sys
import json
import time
from logger import InfoLogger
import os
from file_read_backwards import FileReadBackwards
import Master
#import json

class ELinkManager:



    def __init__(self,master, ground_ip):
        self.master = master
        self.exp_info_logger=master.exp_info_logger
        self.host = ''
        if ground_ip == 'local':
            self.ground_host = socket.gethostname()
        else:
            self.ground_host = ground_ip
        self.ground_host='192.168.1.1' #changeeeeeeeeeeeee
        self.recv_port = 12345
        self.data_port = 12347
        self.logs_port = 12348
        self.BUFFER_SIZE = 1024
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.a=socket.gethostname()
        #print(self.a)
        #self.a=socket.gethostbyname(self.a)
        #print(self.a)
        self.host='0.0.0.0'  #changeeeeeeeeeeeeeee
        #self.host=socket.gethostname()
        self.recv_socket.bind((self.host, self.recv_port))
        self.recv_socket.listen(5)
        self.info_logger=InfoLogger('elink_logger','elink_info.log')
        #last_index = self.get_last_index(file_name)
        #self.last_sended_index = str(last_index)
        self.last_sended_index=1



        self.stop_log_threads = False

        self.start_log_threads()


        #self.thread_elink = threading.Thread(target=self.elink.start).start()
        #self.thread_elink = threading.Thread(target=self.start)
        #self.thread_elink.start()


    def start_log_threads(self):
        """Starts log threads and
            stores them as object attributes
        """
        self.data_log_thread = threading.Thread(target=self.send_logs, args=('data.log',self.data_port,))
        self.data_log_thread.start()
        self.info_log_thread = threading.Thread(target=self.send_logs, args=('info.log',self.logs_port,))
        self.info_log_thread.start()


    def send_logs(self, file_name, port):
        """Sends logs to ground stations

        Arguments:
            file_name {string} -- The log file
            port {int} -- The port
        """
        print('mpika')
        print(port)
        host=self.ground_host
        #host='192.168.1.12'
        while(True):
            if self.stop_log_threads : break

            time.sleep(5)

            ground_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.master.commands['TERMINATE_EXP']==1:
                self.info_logger.write_info('closing logs socket...........')
                ground_socket.close()
            try:
                ground_socket.settimeout(5)
                ground_socket.connect((host, port))
                self.info_logger.write_info ('connected')
                print("log socket connected")
                #self.info_logger.write_info('Connect to ground to port {port} to send {filename}'.format(port=port, filename=file_name))
            except (socket.error , socket.timeout)  as e:
                #self.logger.write_info('error')
                #self.master.info_logger.write_info('Socket Error when trying to connect to ground to send {filename}'.format(filename=file_name))
                time.sleep(2) #wait 2 seconds and retry
                continue

            ground_socket.send(file_name.encode('utf-8'))
            self.info_logger.write_info('sended')
            print("sended")
            temp_string='xaxaxa'
            logger = self.master.exp_info_logger if file_name == 'info.log' else self.master.data_logger
            #ground_socket.send(temp_string.encode('utf-8'));
            unsend_data, total_rows = logger.get_unsend_data()
            print(unsend_data)
            ground_socket.sendall(str(total_rows).encode('utf-8'))
            time.sleep(0.2)

            for log in unsend_data:

                curr_id = log.split(',')[0]
                try:
                    log = '{log}'.format(log=log)
                    ground_socket.sendall(log.encode('utf-8'))
                    response = ground_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                    print('response='+format(response))
                    if response != 'Received':
                        self.info_logger.write_info('connection error')
                        break
                    logger.set_last_sended_index(curr_id)
                    #print(self.last_sended_index)

                    self.info_logger.write_info('recieved')

                except (ConnectionResetError , ConnectionAbortedError) as e:
                    #self.master.info_logger('Lost Connection. Unable to send log {log}'.format(log=log))
                    self.info_logger.write_info('connection error')
                    print("eroooooorrrrr")
                    break
                except socket.timeout:
                    print("eroooooorrrrr2")
                    break
                time.sleep(0.2)

            ground_socket.close()

    def start(self):
        """Initialize ELinkManager. Bind him to await for a connection"""
        while True:
           #start listening
           ground_socket,addr = self.recv_socket.accept()
           #self.master.info_logger.write_info('Got a connection from {addr}'.format(addr=addr))
           #Start Thread to serve client
           self.info_logger.write_info(addr)

           self.con_thread=threading.Thread(target=self.open_connetion,
                            args=(ground_socket, addr,))
           self.con_thread.start()

           #self.open_connetion(ground_socket,addr, )
           #time.sleep(5)
           #self.data_log_thread = threading.Thread(target=self.send_logs, args=('data.log',self.data_port,))
           #self.data_log_thread.start()
           #self.send_logs('xaxa', 8080)


    def open_connetion(self,ground_socket,addr):
        """
            @ground_socket : the connection socket between ground and elinkmanager
            @addr: the ground address
            Function to handle communication with ground software for manual commands
        """
        #send prompt
        a='hi im vayos'
        #self.info_log_thread=threading.Thread(target=self.send_logs, args=('xaxa', 12347))
        #self.info_log_thread.start()
        try:
            ground_socket.send(a.encode('utf-8'))
            while(True):
                #get package as json string
                ground_package_json = ground_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                """if not ground_package_json:
                    self.master.info_logger.write_error('Lost connection unexpectedly from {addr}'.format(addr=addr))
                    break"""
                self.info_logger.write_info(ground_package_json)
                if(ground_package_json)=='TERMINATE_EXP':
                    self.info_logger.write_info('elink sockets closed............')
                    ground_socket.close()
                    #self.recv_socket.close()
                #handle the client package
                server_response = self.handle_package(ground_package_json)

                #send repsonse to client
                ground_socket.send(server_response.encode('utf-8'))

            ground_socket.close()

            #sys.exit()
        except ConnectionResetError:
            print("lost")
            ground_socket.close()
            self.recv_socket.close()  #mporei na xreiastei na allaksei
            #remove this , add log
            #self.master.info_logger.write_error('Lost connection unexpectedly from {addr}'.format(addr=addr))

    def handle_package(self,ground_package_json):
        action=ground_package_json
        """
            @ground_package_json : the package received from ground
            Method to analyse ground's package
            and execute the appropriate actions
        """
        #json to list
        #client_data = json.loads(ground_package_json)
        #get data

        #self.master.info_logger.write_info('Action {action} was received from ground.'.format(action=action))
        if action == 'RESTART_LOGS':
            self.stop_log_threads = True
            #if self.data_log_thread.isAlive():
                #self.data_log_thread.join()
            if self.info_log_thread.is_alive():
                self.info_log_thread.join()
                self.info_logger.write_info('restarted')
            self.stop_log_threads = False
            #self.start_log_threads()
            self.info_log_thread=threading.Thread(target=self.send_logs, args=('xaxa', 12347))
            self.info_log_thread.start()
            return """
                 [+] Command {action} Successfuly
                 [+] restarted log threads
               """.format(action=action)
        elif action =='TERMINATE_EXP':
            self.info_logger.write_info("experiment terminated manually")
            GPIO.output(24, GPIO.LOW)
            self.master.status['valve1'] = 0
            GPIO.output(23, GPIO.LOW)
            self.master.status['valve2'] = 0
            GPIO.output(7, GPIO.LOW)
            self.master.status['pump'] = 0
        elif action== 'OPEN_V1':
            GPIO.output(24,GPIO.HIGH)
            self.info_logger.write_info('valve 1 opened manually')
            self.master.status['valve1']=1
        elif action== 'CLOSE_V1':
            GPIO.output(24,GPIO.LOW)
            self.info_logger.write_info('valve 1 closed manually')
            self.master.status['valve1']=0
        elif action== 'OPEN_V2':
            GPIO.output(23,GPIO.HIGH)
            self.info_logger.write_info('valve 2 opened manually')
            self.master.status['valve2']=1
        elif action== 'CLOSE_V2':
            GPIO.output(23,GPIO.LOW)
            self.info_logger.write_info('valve 2 closed manually')
            self.master.status['valve2']=0
        elif action== 'TON_H1':
            GPIO.output(17,GPIO.HIGH)
            self.info_logger.write_info('heater 1 turned on manually')
            self.master.status['heater1']=1
        elif action== 'TOFF_H1':
            GPIO.output(17,GPIO.LOW)
            self.info_logger.write_info('heater 1 turned off manually')
            self.master.status['heater1']=0
        elif action== 'TON_H2':
            GPIO.output(18,GPIO.HIGH)
            self.info_logger.write_info('heater 2 turned on manually')
            self.master.status['heater2']=1
        elif action== 'TOFF_H2':
            GPIO.output(18,GPIO.LOW)
            self.info_logger.write_info('heater 2 turned off manually')
            self.master.status['heater2']=0
        elif action== 'TON_PUMP':
            GPIO.output(7,GPIO.HIGH)
            self.info_logger.write_info('pump turned on manually')
            self.master.status['pump']=1
        elif action== 'TOFF_PUMP':
            GPIO.output(7,GPIO.LOW)
            self.info_logger.write_info('pump turned off manually')
            self.master.status['pump']=0

        elif action== 'STAGE_1':
            self.master.commands['STAGE_1']=1

        elif action== 'STAGE_2':
            self.master.commands['STAGE_2']=1

        elif action== 'STAGE_3':
            self.master.commands['STAGE_3']=1

        elif action== 'NEW_CYCLE':
            self.master.commands['NEW_CYCLE']=1

        else:
            self.master.commands[action] = 1
            return """
                           [+] Command {action} Successfuly
                           [+] changed command_vector
                        """.format(action=action)





