import multiplexer
import pump_for_test
import valve_for_test
import time
import csv


pump=pump_for_test.pump_for_test()
valve=valve_for_test.valve()
multiplex = multiplexer.multiplex(1)
valve.open_valve()
pump.ton_pump()
multiplex.channel(0x70, 7)
press=0

with open('press.csv', 'a+', newline='') as file:
    writer = csv.writer(file)
    row = ['Time', 'Press']
    writer.writerow(row)

while press<2000:
    press, temp = multiplex.get_press(7)
    print("press="+format(press))

pump.toff_pump()
valve.close_valve()
last_time = int(round(time.time() * 1000))
while (int(int(round(time.time() * 1000)) - last_time))< 180000:
    press, temp = multiplex.get_press(7)
    with open('press.csv', 'a+', newline='') as file:
        writer = csv.writer(file)
        row = [press]
        writer.writerow(row)
    print("press=" + format(press))
    time.sleep(1)


