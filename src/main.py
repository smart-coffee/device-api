# import serial
# ser = serial.Serial('/dev/ttyS0',115200)

# print(ser)

# while True:
#     print(ser.readline().decode("utf-8"))

#####

# from smbus2 import SMBus

# bus = SMBus(1)
# # Register addresses (with "normal mode" power-down bits)
# reg_write_dac = 0x40
# address = 0x60
# voltage = 0xaaa

# msg = (voltage & 0xff0) >> 4
# msg = [msg, (msg & 0xf) << 4]

# bus.write_i2c_block_data(address, reg_write_dac, msg)

import RPi.GPIO as GPIO
import time


gpios = {
    4: [],
    17: [],
    27: [],
    22: [],
    5: [],
    6: [],
    13: [],
    19: []
}


GPIO.setmode(GPIO.BCM)
for gpio in gpios.keys():
    GPIO.setup(gpio, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

reads = []

for gpio, values in gpios.items():
    for i in range(0, 20):
        _val = GPIO.input(gpio)
        _i_str = str(i).zfill(4)
        _time_in_milli = int(round(time.time() * 1000))
        reads.append((gpio, _val, _i_str, _time_in_milli))



for i in reads:
    print('{0} {1}: {2} {3}'.format(*i))
