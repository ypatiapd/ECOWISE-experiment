#import serial
import numpy as np

import re

class gps:

    __instance= None

    def __init__(self):
        self.message=None
        self.dictionary=dict()
        self.lattitude=None
        self.longtitude=None
        self.time=None
        self.checksum=None
        self.status=None

        #ser = serial.Serial('serial0', 38400)

    def init_dict(self):

        self.dictionary["Lattitude"]=None
        self.dictionary["Longtitude"]=None
        self.dictionary["Time"]=None
        self.dictionary["Checksum"] = None
        self.dictionary["Status"]=None


    def read_data(self):
        self.init_dict()

        #for b in ser.read()
        #data=data+b
        #if b=='<LF>':
        #print("data acc completed")
        #break
        #kai metasximatismos tou minimatos
        #apo byte se string me decode()
        self.message="$GPGLL,4717.11634,N,00833.91297,E,124923.00,A,A*6E<CR><LF>"
        self.parse_strings()
        if self.status=='A' :
            print("all good ,store results")
            self.dictionary["Lattitude"] = self.lattitude
            self.dictionary["Longtitude"] = self.longtitude
            self.dictionary["Time"] = self.time
            self.dictionary["Checksum"] = self.checksum

            return self.lattitude, self.longtitude,self.time
        else:
            print("invalid data , didnt store")

    def parse_strings(self):

         parsed_strings = []
         parsed_strings = self.message.split(",")
         check_parse1 = parsed_strings[7].split('*')
         check_parse2 = check_parse1[1].split('<')
         self.checksum = int(check_parse2[0], 16)
         self.lattitude = float(parsed_strings[1])
         self.longtitude = float(parsed_strings[3])
         self.time = float(parsed_strings[5])
         self.status = parsed_strings[6]
