#import serial
import numpy as np
import serial  # to read from serial UART
import pynmea2  # NMEA GPS splitter
from datetime import datetime
from time import sleep
import re
import string

class gps:

    __instance= None

    def __init__(self):
        self.message=None
        self.dictionary=dict()
        self.lattitude=0
        self.longtitude=0
        self.time=0
        self.checksum=None
        self.status=None
        self.port = "/dev/ttyS0"
        self.ser = serial.Serial(self.port, baudrate=9600, timeout=1)

        #ser = serial.Serial('serial0', 38400)

    def init_dict(self):

        self.dictionary["Lattitude"]=0
        self.dictionary["Longtitude"]=0
        self.dictionary["Time"]=0
        self.dictionary["Checksum"] = None
        self.dictionary["Status"]=None

    def read_data2(self):
        lat=0
        lng=0
        dataout = pynmea2.NMEAStreamReader()

        counter=0
        while counter<100:
            """if newdata.find(b'GGA') > 0:
                msg = pynmea2.parse(newdata.decode('utf-8'))"""
            newdata = self.ser.readline()
            newdata = newdata.decode("utf-8", "ignore")
            #print(format(newdata))
            if newdata[0:6] == "$GPGGA":
                #print("newdata="+newdata)
                newmsg = pynmea2.parse(newdata)
                lat = newmsg.latitude
                #print("lat="+format(lat))
                lng = newmsg.longitude
                #print("lng=" + format(lng))
                return lat, lng
                latlng = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
            counter+=1
