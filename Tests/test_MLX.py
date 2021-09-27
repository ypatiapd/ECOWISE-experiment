from smbus2 import SMBus
from mlx90614 import MLX90614

bus=SMBus(1)
sensor=MLX90614(bus,address=0x19)
a=sensor.get_ambient()
print("ambient temperature="+format(a))
b=sensor.get_object_1()
print("object1 temperature="+format(b))
c=sensor.get_object_2()
print("object2 temperature="+format(c))

bus.close()
