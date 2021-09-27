import serial
import time
import string
import pynmea2


def main():
    port="/dev/ttyS0"
    ser=serial.Serial(port, baudrate=9600, timeout=1)
    while(True):
        read_data2(ser)

def read_data2(ser):
    lat=0
    lng=0
    dataout = pynmea2.NMEAStreamReader()

    counter=0
    while counter<100:
        """if newdata.find(b'GGA') > 0:
            msg = pynmea2.parse(newdata.decode('utf-8'))"""
        newdata = ser.readline()
        newdata = newdata.decode("utf-8", "ignore")
        print(format(newdata))
        if newdata[0:6] == "$GPGGA":
            #print("newdata="+newdata)
            newmsg = pynmea2.parse(newdata)
            lat = newmsg.latitude
            print("lat="+format(lat))
            lng = newmsg.longitude
            print("lng=" + format(lng))
            alt = newmsg.altitude
            print("alt="+format(alt))
            return lat, lng , alt
        counter+=1

if __name__ == '__main__':
    main()
