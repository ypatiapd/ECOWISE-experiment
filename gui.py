# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 19:39:51 2020

@author: vayos
"""
from tkinter import *
import tkinter as tk
from tkinter import StringVar, IntVar
from functools import partial
import ground
import threading

from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def updateValues():

    svalue1 = int(c.status["pump"])
    svalue2 = int(c.status["valve1"])
    svalue3 = int(c.status["valve2"])
    svalue4 = int(c.status["heater1"])
    svalue5 = int(c.status["heater2"])
    svalue6 = int(c.stages["stage1"])
    svalue7 = int(c.stages["stage2"])
    svalue8 = int(c.stages["stage3"])

    value1 = str(c.data["In_Hum"])
    value2 = str(c.data["Out_Hum"])
    value3 = str(c.data["In_Press"])
    value4 = str(c.data["Out_Press"])
    value5 = str(c.data["In_Temp"])
    value6 = str(c.data["Out_Temp"])
    value7 = str(c.data["CO2_1"])
    value8 = str(c.data["CO2_2"])
    value9 = str(c.data["O3_1"])
    value10 = str(c.data["O3_2"])
    value11 = str(c.data["Gps_X"])
    value12 = str(c.data["Gps_Y"])
    value13 = str(c.data["Gps_altitude"])
    value14 = str(c.data["Pump_Temp"])
    value15 = str(c.data["SB_Temp"])


    if svalue1 >= 1:
        pump.set("opened")
        label1.config(bg="green")
        # button1.config(bg="green", fg="black")
        # button2.config(bg="white", fg="black")
    else:
        pump.set("closed")
        label1.config(bg="red")
        # button1.config(bg="white", fg="black")
        # button2.config(bg="red", fg="black")
    if svalue2 >= 1:
        valve1.set("opened")
        label2.config(bg="green")
        # button3.config(bg="green", fg="black")
        # button4.config(bg="white", fg="black")
    else:
        valve1.set("closed")
        label2.config(bg="red")
        # button3.config(bg="white", fg="black")
        # button4.config(bg="red", fg="black")
    if svalue3 >= 1:
        valve2.set("opened")
        label3.config(bg="green")
        # button5.config(bg="green", fg="black")
        # button6.config(bg="white", fg="black")
    else:
        valve2.set("closed")
        label3.config(bg="red")
        # button5.config(bg="white", fg="black")
        # button6.config(bg="red", fg="black")
    if svalue4 >= 1:
        heater1.set("opened")
        label4.config(bg="green")
        # button7.config(bg="green", fg="black")
        # button8.config(bg="white", fg="black")
    else:
        heater1.set("closed")
        label4.config(bg="red")
        # button7.config(bg="white", fg="black")
        # button8.config(bg="red", fg="black")
    if svalue5 >= 1:
        heater2.set("opened")
        label5.config(bg="green")
        # button9.config(bg="green", fg="black")
    # button10.config(bg="white", fg="black")
    else:
        heater2.set("closed")
        label5.config(bg="red")
        # button9.config(bg="white", fg="black")
        # button10.config(bg="red", fg="black")

    if svalue6 >= 1:
        stage.set("stage1")
        # button11.config(bg="green", fg="black")
        # button12.config(bg="white", fg="black")
        # button13.config(bg="white", fg="black")
    elif svalue7 >= 1:
        stage.set("stage2")
        # button12.config(bg="green", fg="black")
        # button11.config(bg="white", fg="black")
        # button13.config(bg="white", fg="black")
    else:
        stage.set("stage3")
        # button13.config(bg="green", fg="black")
        # button12.config(bg="white", fg="black")
        # button11.config(bg="white", fg="black")

    humin.set(value1)
    humout.set(value2)
    pressin.set(value3)
    tempin.set(value5)
    pressout.set(value4)
    tempout.set(value6)
    co21.set(value7)
    co22.set(value8)
    o31.set(value9)
    o32.set(value10)
    gpsx.set(value11)
    gpsy.set(value12)
    gpsalt.set(value13)
    pumptemp.set(value14)
    senstemp.set(value15)

    root.after(1000, updateValues)


# Driver code
if __name__ == "__main__":
    c = ground.ground(2)
    thread = threading.Thread(target=c.establish_connection)
    thread.start()

    # Create a GUI window
    root = Tk()
    StringVar()

    # Set the background colour of GUI window
    root.configure(background='pink')

    # Set the configuration of GUI window
    root.geometry("1080x660")
    root.resizable(width=True, height=True)
    root.title("Eco-wise experiment")  # set the title of GUI window
    style.use('bmh')

    pump = tk.StringVar()
    valve1 = tk.StringVar()
    valve2 = tk.StringVar()
    heater1 = tk.StringVar()
    heater2 = tk.StringVar()
    stage = tk.StringVar()
    stage2 = tk.StringVar()
    stage3 = tk.StringVar()

    humin = tk.StringVar()
    humout = tk.StringVar()
    pressin = tk.StringVar()
    pressout = tk.StringVar()
    tempin = tk.StringVar()
    tempout = tk.StringVar()
    co21 = tk.StringVar()
    co22 = tk.StringVar()
    o31 = tk.StringVar()
    o32 = tk.StringVar()
    gpsx = tk.StringVar()
    gpsy = tk.StringVar()
    gpsalt = tk.StringVar()
    pumptemp = tk.StringVar()
    senstemp = tk.StringVar()

    svalue1 = int(c.status["pump"])
    svalue2 = int(c.status["valve1"])
    svalue3 = int(c.status["valve2"])
    svalue4 = int(c.status["heater1"])
    svalue5 = int(c.status["heater2"])
    svalue6 = int(c.stages["stage1"])
    svalue7 = int(c.stages["stage2"])
    svalue8 = int(c.stages["stage3"])

    value1 = str(c.data["In_Hum"])
    value2 = str(c.data["Out_Hum"])
    value3 = str(c.data["In_Press"])
    value4 = str(c.data["Out_Press"])
    value5 = str(c.data["In_Temp"])
    value6 = str(c.data["Out_Temp"])
    value7 = str(c.data["CO2_1"])
    value8 = str(c.data["CO2_2"])
    value9 = str(c.data["O3_1"])
    value10 = str(c.data["O3_2"])
    value11 = str(c.data["Gps_X"])
    value12 = str(c.data["Gps_Y"])
    value13 = str(c.data["Gps_altitude"])
    value14 = str(c.data["Pump_Temp"])
    value15 = str(c.data["SB_Temp"])

    pump.set("closed")
    valve1.set("closed")
    valve2.set("closed")
    heater1.set("closed")
    heater2.set("closed")
    stage.set("stages")


    humin.set(value1)
    humout.set(value2)
    pressin.set(value3)
    tempin.set(value5)
    pressout.set(value4)
    tempout.set(value6)
    co21.set(value7)
    co22.set(value8)
    o31.set(value9)
    o32.set(value10)
    gpsx.set(value11)
    gpsy.set(value12)
    gpsalt.set(value13)
    pumptemp.set(value14)
    senstemp.set(value15)

    # tkinter labels
    label1 = tk.Label(root, textvariable=pump, fg="black", highlightthickness=4, bd=5)
    label2 = tk.Label(root, textvariable=valve1, fg="black", highlightthickness=4, bd=5)
    label3 = tk.Label(root, textvariable=valve2, fg="black", highlightthickness=4, bd=5)
    label4 = tk.Label(root, textvariable=heater1, fg="black", highlightthickness=4, bd=5)
    label5 = tk.Label(root, textvariable=heater2, fg="black", highlightthickness=4, bd=5)
    label6 = tk.Label(root, textvariable=stage, fg="black", highlightthickness=4, bd=5, bg="pink", font=(14))

    label7 = tk.Label(root, text='Humidity in/out', fg="black", bg="blue", highlightthickness=4, bd=5)
    label8 = tk.Label(root, text='Pressure in/out', fg="black", bg="grey", highlightthickness=4, bd=5)
    label9 = tk.Label(root, text='Temperature in/out', fg="black", bg="orange", highlightthickness=4, bd=5)
    label10 = tk.Label(root, text='Co2 1/2', fg="black", bg="#0796ba", highlightthickness=4, bd=5)
    label11 = tk.Label(root, text='O3 1/2', fg="black", bg="#9607ba", highlightthickness=4, bd=5)
    label12 = tk.Label(root, text='GPS', fg="black", highlightthickness=4, bd=5, font=14)
    label13 = tk.Label(root, text='Pump/sensor tmperature', fg="black", bg="#86bd08", highlightthickness=4, bd=5)
    # label14 = tk.Label(root, text = 'Sensor temperature', fg="black", highlightthickness=4, bd=10)

    label15 = tk.Label(root, textvariable=humin, fg="blue", bg="pink", font=(20))
    label16 = tk.Label(root, textvariable=humout, fg="blue", bg="pink", font=(20))
    label17 = tk.Label(root, textvariable=pressin, fg="grey", bg="pink", font=(20))
    label18 = tk.Label(root, textvariable=tempin, fg="orange", bg="pink", font=(20))
    label19 = tk.Label(root, textvariable=pressout, fg="grey", bg="pink", font=(20))
    label20 = tk.Label(root, textvariable=tempout, fg="orange", bg="pink", font=(20))
    # label21 = tk.Label(root, text = 'kati allo', fg="black")
    label22 = tk.Label(root, textvariable=co21, fg="#0796ba", bg="pink", font=(20))
    label23 = tk.Label(root, textvariable=co22, fg="#0796ba", bg="pink", font=(20))
    label24 = tk.Label(root, textvariable=o31, fg="#9607ba", bg="pink", font=(20))
    label25 = tk.Label(root, textvariable=o32, fg="#9607ba", bg="pink", font=(20))
    label26 = tk.Label(root, textvariable=gpsx, fg="black", bg="pink", font=(20))
    label27 = tk.Label(root, textvariable=gpsy, fg="black", bg="pink", font=(20))
    label28 = tk.Label(root, textvariable=gpsalt, fg="black", bg="pink", font=(20))
    label29 = tk.Label(root, textvariable=pumptemp, fg="#86bd08", bg="pink", font=(20))
    label30 = tk.Label(root, textvariable=senstemp, fg="#86bd08", bg="pink", font=(20))
    # label31 = tk.Label(root, text = 'status', fg="black", highlightthickness=4, bd=5)

    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure
    label1.grid(row=1, column=3, sticky=W, ipadx=45)
    label2.grid(row=2, column=3, sticky=W, ipadx=45)
    label3.grid(row=3, column=3, sticky=W, ipadx=45)
    label4.grid(row=4, column=3, sticky=W, ipadx=45)
    label5.grid(row=5, column=3, sticky=W, ipadx=45)
    label6.grid(row=6, rowspan=2, column=3, sticky=W, ipadx=53, ipady=16)
    label7.grid(row=1, column=4, ipadx=45)
    label8.grid(row=2, column=4, ipadx=48)
    label9.grid(row=3, column=4, ipadx=37)
    label10.grid(row=5, column=4, ipadx=68)
    label11.grid(row=6, column=4, ipadx=71)
    label12.grid(row=7, rowspan=2, column=4, ipadx=70, ipady=19)
    label13.grid(row=4, column=4, ipadx=22)
    # label14.grid(row = 5, column = 4, ipadx = 45)
    label15.grid(row=1, column=5, ipadx=45)
    label16.grid(row=1, column=6, ipadx=45)
    label17.grid(row=2, column=5, ipadx=40)
    label18.grid(row=3, column=5, ipadx=40)
    label19.grid(row=2, column=6, ipadx=40)
    label20.grid(row=3, column=6, ipadx=40)
    # label21.grid(row = 16, column = 3, ipadx = 45)
    label22.grid(row=5, column=5, ipadx=45)
    label23.grid(row=5, column=6, ipadx=45)
    label24.grid(row=6, column=5, ipadx=45)
    label25.grid(row=6, column=6, ipadx=45)
    label26.grid(row=7, column=5, ipadx=45)
    label27.grid(row=7, column=6, ipadx=45)
    label28.grid(row=8, column=5, columnspan=2, ipadx=45)
    label29.grid(row=4, column=5, ipadx=35)
    label30.grid(row=4, column=6, ipadx=40)
    # label31.grid(row = 8, column = 3, ipadx = 70)

    # tkinter buttons
    button1 = Button(root, text="open pump", fg='green', command=partial(c.send_command, 'TON_PUMP'),
                     highlightthickness=4, bd=5)
    button2 = Button(root, text="close pump", fg='red', command=partial(c.send_command, 'TOFF_PUMP'),
                     highlightthickness=4, bd=5)
    button3 = Button(root, text="open valve 1", fg='green', command=partial(c.send_command, 'OPEN_VALVE1'),
                     highlightthickness=4, bd=5)
    button4 = Button(root, text="close valve 1", fg='red', command=partial(c.send_command, 'CLOSE_VALVE1'),
                     highlightthickness=4, bd=5)
    button5 = Button(root, text="open valve 2", fg='green', command=partial(c.send_command, 'OPEN_VALVE2'),
                     highlightthickness=4, bd=5)
    button6 = Button(root, text="close valve 2", fg='red', command=partial(c.send_command, 'CLOSE_VALVE2'),
                     highlightthickness=4, bd=5)
    button7 = Button(root, text="open heater 1", fg='green', command=partial(c.send_command, 'TON_H1'),
                     highlightthickness=4, bd=5)
    button8 = Button(root, text="close heater 1", fg='red', command=partial(c.send_command, 'TOFF_H1'),
                     highlightthickness=4, bd=5)
    button9 = Button(root, text="open heater 2", fg='green', command=partial(c.send_command, 'TON_H2'),
                     highlightthickness=4, bd=5)
    button10 = Button(root, text="close heater 2", fg='red', command=partial(c.send_command, 'TOFF_H2'),
                      highlightthickness=4, bd=5)
    button11 = Button(root, text="stage 1", fg='black', command=partial(c.send_command, 'STAGE_1'),
                      highlightthickness=4, bd=5)
    button12 = Button(root, text="stage 2", fg='black', command=partial(c.send_command, 'STAGE_2'),
                      highlightthickness=4, bd=5)
    button13 = Button(root, text="stage 3", fg='black', command=partial(c.send_command, 'STAGE_3'),
                      highlightthickness=4, bd=5)
    button14 = Button(root, text="new cycle", fg='black', command=partial(c.send_command, 'NEW_CYCLE'),
                      highlightthickness=4, bd=5)
    button15 = Button(root, text="restart", command=partial(c.send_command, 'RESTART_LOGS'), highlightthickness=4, bd=5)
    button16 = Button(root, text="terminate experiment", command=partial(c.send_command, 'TERMINATE_EXP'),
                      highlightthickness=4, bd=5)

    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure
    button1.grid(row=1, column=1, sticky=W, ipadx='35')
    button2.grid(row=1, column=2, sticky=W, ipadx='35')
    button3.grid(row=2, column=1, sticky=W, ipadx='33')
    button4.grid(row=2, column=2, sticky=W, ipadx='33')
    button5.grid(row=3, column=1, sticky=W, ipadx='33')
    button6.grid(row=3, column=2, sticky=W, ipadx='33')
    button7.grid(row=4, column=1, sticky=W, ipadx='30')
    button8.grid(row=4, column=2, sticky=W, ipadx='30')
    button9.grid(row=5, column=1, sticky=W, ipadx='30')
    button10.grid(row=5, column=2, sticky=W, ipadx='30')
    button11.grid(row=6, column=1, sticky=W, ipadx='48')
    button12.grid(row=6, column=2, sticky=W, ipadx='48')
    button13.grid(row=7, column=1, sticky=W, ipadx='48')
    button14.grid(row=7, column=2, sticky=W, ipadx='41')
    button15.grid(row=8, column=1, ipadx='50')
    button16.grid(row=8, column=2, ipadx='10')

    # figure represents the graphic part of the system
    """figure = Figure(figsize=(5, 3), facecolor='pink', frameon=True)
    figure1 = Figure(figsize=(5, 3), facecolor='pink', frameon=True)
    #figure2 = Figure(figsize=(4, 3), facecolor='pink', frameon=True)
    #figure.add_gridspec(10,10)

    canvas = FigureCanvasTkAgg(figure, root)
    canvas.get_tk_widget().grid(row=0, columnspan=4, sticky=W)
    canvas1 = FigureCanvasTkAgg(figure1, root)
    canvas1.get_tk_widget().grid(row=0, column=4, columnspan=3)
    #canvas2 = FigureCanvasTkAgg(figure2, root)
    #canvas2.get_tk_widget().grid(row=0, column=4, columnspan=3)

    newAnimation = c.nt(figure)
    newAnimation1 = c.nt1(figure1)
    #newAnimation2 = c.nt2(figure2)"""

    # Update values
    root.after(1000, updateValues)

    # Start the GUI
    root.mainloop()
