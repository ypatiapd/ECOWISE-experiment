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
import RPi.GPIO as GPIO
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
        self.ground_host='192.168.1.4' #ground ip
        self.recv_port = 12345
        self.data_port = 12347
        self.logs_port = 12348
        self.BUFFER_SIZE = 1024
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host='0.0.0.0'  #if 2 pcs we leave the google host, if one pc,  we put gethostname()
        #self.host=socket.gethostname()
        self.recv_socket.bind((self.host, self.recv_port))  #this socket always listens
        self.recv_socket.listen(5)
        self.info_logger=InfoLogger('elink_logger','elink_info.log')
        #last_index = self.get_last_index(file_name)
        #self.last_sended_index = str(last_index)
        self.last_sended_index=1
        self.stop_log_threads = False
        self.start_log_threads()


    def start_log_threads(self):
        """Starts log threads and
            stores them as object attributes
        """
        self.data_log_thread = threading.Thread(target=self.send_logs, args=('data.log',self.data_port,))
        self.data_log_thread.start()
        #self.info_log_thread = threading.Thread(target=self.send_logs, args=('info.log',self.logs_port,))
        #self.info_log_thread.start()


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

            #time.sleep(5)

            ground_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.master.commands['TERMINATE_EXP']==1:
                self.info_logger.write_info('Terminating experiment...Closing logs socket...........')
                self.exp_info_logger.write_info('Terminating experiment...Closing logs socket...........')
                print("elink thread terminating...")
                ground_socket.close()
                return -1
            try:
                ground_socket.settimeout(5)
                ground_socket.connect((host, port))
                self.info_logger.write_info('Connect to ground to port {port} to send {filename}'.format(port=port, filename=file_name))
                self.exp_info_logger.write_info('Connect to ground to port {port} to send {filename}'.format(port=port, filename=file_name))
            except (socket.error , socket.timeout)  as e:
                self.info_logger.write_info('Socket Error when trying to connect to ground to send {filename}'.format(filename=file_name))
                self.exp_info_logger.write_info('Socket Error when trying to connect to ground to send {filename}'.format(filename=file_name))
                time.sleep(2) #wait 2 seconds and retry
                continue

            ground_socket.send(file_name.encode('utf-8'))   # firstly we send the filename
            logger = self.master.exp_info_logger if file_name == 'info.log' else self.master.data_logger
            unsend_data, total_rows = logger.get_unsend_data()
            ground_socket.sendall(str(total_rows).encode('utf-8'))  #then we send the number of rows of unsend data
            time.sleep(0.2)

            for log in unsend_data:

                curr_id = log.split(',')[0]
                try:
                    log = '{log}'.format(log=log)
                    ground_socket.sendall(log.encode('utf-8'))  #then we send the unsend data
                    response = ground_socket.recv(self.BUFFER_SIZE).decode('utf-8')  #ground response
                    if response != 'Received':
                        self.exp_info_logger.write_info('Error..Didnt receive response from ground socket')
                        self.info_logger.write_info('Error..Didnt receive response from ground socket')

                        break
                    logger.set_last_sended_index(curr_id)

                except (ConnectionResetError , ConnectionAbortedError) as e:
                    self.exp_info_logger.write_info('Lost Connection. Unable to send log {log}'.format(log=log))
                    self.info_logger.write_info('Lost Connection. Unable to send log {log}'.format(log=log))
                    break
                except socket.timeout:
                    self.exp_info_logger.write_info('Lost Connection. Unable to send log {log}'.format(log=log))
                    self.info_logger.write_info('Lost Connection. Unable to send log {log}'.format(log=log))
                    print("eroooooorrrrr2")
                    break
                time.sleep(0.2)

            ground_socket.close()

    def start(self):
        """Initialize ELinkManager. Bind him to await for a connection"""
        while True:
           #start listening
           print("akouw")
           ground_socket,addr = self.recv_socket.accept()# AYTO PARAMENEI ANOIXTO prepei na kleisei alla pws
           if self.master.commands['TERMINATE_EXP'] == 1:  #auto einai axristo logika
               print("elink thread terminating...")
               ground_socket.close()
               return
           self.info_logger.write_info('Got a connection from {addr}'.format(addr=addr))
           self.exp_info_logger.write_info('Got a connection from {addr}'.format(addr=addr))
           #Start Thread to serve client

           self.con_thread=threading.Thread(target=self.open_connetion,
                            args=(ground_socket, addr,))
           self.con_thread.start()


    def open_connetion(self,ground_socket,addr):
        """
            @ground_socket : the connection socket between ground and elinkmanager
            @addr: the ground address
            Function to handle communication with ground software for manual commands
        """
        #send prompt

        a = 'hi im vayos'

        try:
            ground_socket.send(a.encode('utf-8'))
            while(True):
                #get package as json string
                ground_package_json = ground_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                if not ground_package_json:
                    self.master.info_logger.write_error('Lost connection unexpectedly from {addr}'.format(addr=addr))
                    break
                self.info_logger.write_info(ground_package_json)
                server_response = self.handle_package(ground_package_json)
                if (ground_package_json) == 'TERMINATE_EXP':
                    self.info_logger.write_info('Terminating experiment...elink sockets closed............')
                    self.exp_info_logger.write_info('Terminating experiment...elink sockets closed............')
                    print("elink thread terminating...")
                    ground_socket.close()
                    self.recv_socket.close()
                    return -1
                    break
                #send repsonse to client
                ground_socket.send(server_response.encode('utf-8'))

            ground_socket.close()

            #sys.exit()
        except ConnectionResetError:
            print("lost")
            self.info_logger.write_info('connection error in commands connection sockets')
            self.info_logger.write_info('connection error in commmands connection sockets')
            ground_socket.close()
            self.recv_socket.close()  #mporei na xreiastei na allaksei
            #remove this , add log
            #self.master.info_logger.write_error('Lost connection unexpectedly from {addr}'.format(addr=addr))

    def handle_package(self,ground_package_json):
        action=ground_package_json
        print(format(action))
        """
            @ground_package_json : the package received from ground
            Method to analyse ground's package
            and execute the appropriate actions
        """
        #json to list
        #client_data = json.loads(ground_package_json)
        #get data

        #self.master.info_logger.write_info('Action {action} was received from ground.'.format(action=action))
        if action == 'RESTART_LOGS':  # doulepse to den to xeis dei
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
            self.exp_info_logger.write_info(" Successfuly restarted log threads manually")
            return """Command {action} Successfuly restarted log threads""".format(action=action)
        #elif action == "RELOAD_CONN":
        #    return """
        #                 [+] Command {action} successfuly
        #                 [+] reload connection
        #               """.format(action=action)

        else:
            self.master.commands[action] = 1
            self.exp_info_logger.write_info("Command {action} Successully changed command_vector""".format(action=action))
            return """Command {action} Successully changed command_vector""".format(action=action)








