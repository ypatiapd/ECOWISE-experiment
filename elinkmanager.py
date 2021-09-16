# -*- coding: utf-8 -*-
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
        self.host = ''
        if ground_ip == 'local':
            self.ground_host = socket.gethostname()
        else:
            self.ground_host = ground_ip
        self.ground_host='192.168.1.1' #ground ip
        self.recv_port = 12345
        self.data_port = 12347
        self.logs_port = 12348
        self.BUFFER_SIZE = 1024
        self.connection_lost=0

        self.info_logger=InfoLogger('elink_logger','elink_info.log')
        self.stop_log_threads = False
        self.start_log_threads()

    def start_log_threads(self):
        """Starts log threads and
            stores them as object attributes
        """
        self.data_log_thread = threading.Thread(target=self.send_logs, args=('data.log',self.data_port,))
        self.data_log_thread.start()

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
            ground_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.master.commands['TERMINATE_EXP']==1:
                self.info_logger.write_info('Terminating experiment...Closing logs socket...........')
                print("elink thread terminating...")
                ground_socket.close()
                return -1
            try:
                ground_socket.settimeout(5)
                ground_socket.connect((host, port))
                self.info_logger.write_info('Connect to ground to port {port} to send {filename}'.format(port=port, filename=file_name))
            except (socket.error , socket.timeout,ConnectionAbortedError)  as e:
                self.info_logger.write_info('Socket Error when trying to connect to ground to send {filename}'.format(filename=file_name))
                self.connection_lost=1
                ground_socket.close()
                time.sleep(2) #wait 2 seconds and retry
                continue

            ground_socket.send(file_name.encode('utf-8'))   # firstly we send the filename
            time.sleep(0.2)
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
                        self.info_logger.write_info('Error..Didnt receive response from ground socket')
                        break
                    logger.set_last_sended_index(curr_id)

                except (socket.error,ConnectionResetError , ConnectionAbortedError) as e:
                    self.info_logger.write_info('Lost Connection. Unable to send log {log}'.format(log=log))
                    self.connection_lost=1
                    ground_socket.close()
                    break
                except socket.timeout:
                    self.connection_lost=1
                    self.info_logger.write_info('Lost Connection. Unable to send log {log}'.format(log=log))
                    ground_socket.close()
                    break
                time.sleep(0.2)

            ground_socket.close()

    def open_connetion(self):
        """
            @ground_socket : the connection socket between ground and elinkmanager
            @addr: the ground address
            Function to handle communication with ground software for manual commands
        """
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host = '0.0.0.0'  # if 2 pcs we leave the google host, if one pc,  we put gethostname()
        # self.host=socket.gethostname()
        recv_socket.bind((host, self.recv_port))  # this socket always listens
        recv_socket.listen(5)

        while (True):
            # start listening
            try:
                self.info_logger.write_info("mpika start")
                ground_socket, addr = recv_socket.accept()  # AYTO PARAMENEI ANOIXTO prepei na kleisei alla pws
                ground_socket.setblocking(False)
                ground_socket.settimeout(5)
                self.info_logger.write_info("to prosperasa")
            except(OSError):
                print("den sindethika")
                continue
            self.info_logger.write_info('Got a connection from {addr}'.format(addr=addr))
            # Start Thread to serve client
            a = 'hi im vayos'
            try:
                ground_socket.send(a.encode('utf-8'))

            except (socket.timeout, ConnectionResetError, ConnectionAbortedError, TimeoutError):
                print("lost")
                self.info_logger.write_info('connection error in commands connection sockets')
                continue
            while(True):
                try:
                    #get package as json string
                    ground_package_json = ground_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                    if not ground_package_json:
                        self.info_logger.write_error('Lost connection unexpectedly from {addr}'.format(addr=addr))

                        break
                    self.info_logger.write_info(ground_package_json)
                    server_response = self.handle_package(ground_package_json)
                    if (ground_package_json) == 'TERMINATE_EXP':
                        self.info_logger.write_info('Terminating experiment...commands socket closed............')
                        print("elink thread terminating...")
                        ground_socket.close()
                        return -1
                    #send repsonse to client
                    ground_socket.send(server_response.encode('utf-8'))
                except(BlockingIOError):
                    print("not received anything")
                    self.info_logger.write_info('Not received anything')
                    continue
                except (socket.timeout, ConnectionResetError, ConnectionAbortedError, TimeoutError):
                    print("Timeout")
                    self.info_logger.write_info('Timeout')
                    ground_socket.close()
                    break

    def handle_package(self,ground_package_json):
        action=ground_package_json
        print(format(action))
        """
            @ground_package_json : the package received from ground
            Method to analyse ground's package
            and execute the appropriate actions
        """
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
            return """Command {action} Successfuly restarted log threads""".format(action=action)
        elif action=="NC":
            return "AG"
        else:
            self.master.commands[action] = 1
            self.info_logger.write_info("Command {action} Successully changed command_vector""".format(action=action))
            return """Command {action} Successully changed command_vector""".format(action=action)








