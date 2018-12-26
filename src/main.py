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


class GPIORead:
    def __init__(self, gpio_number: int, value: bool, time_in_milli: int):
        self.gpio_number = gpio_number
        self.value = value
        self.time_in_milli = time_in_milli
    
    def __repr__(self):
        #return str(self.__dict__)
        gpio_number_str = str(self.gpio_number).zfill(2)
        time_str = self.time_in_milli
        value_str = self.value
        return '{0} {1}: {2}'.format(gpio_number_str, time_str, value_str)


gpio_numbers = [4, 17, 27, 22, 5, 6, 13, 19]


GPIO.setmode(GPIO.BCM)
for gpio in gpio_numbers:
    GPIO.setup(gpio, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

reads = []

for gpio in gpio_numbers:
    _found_high = False
    for i in range(0, 100):
        _val = GPIO.input(gpio)
        if _val == GPIO.HIGH:
            _found_high = True
            _time_in_milli = int(round(time.time() * 1000))
            reads.append(GPIORead(gpio_number=gpio, value=True, time_in_milli=_time_in_milli))
            break
    if not _found_high:
        _time_in_milli = int(round(time.time() * 1000))
        reads.append(GPIORead(gpio_number=gpio, value=False, time_in_milli=_time_in_milli))




for i in reads:
    print(i)
