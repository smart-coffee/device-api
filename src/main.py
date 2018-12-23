# import serial
# ser = serial.Serial('/dev/ttyS0',115200)

# print(ser)

# while True:
#     print(ser.readline().decode("utf-8"))

#####

from smbus2 import SMBus

bus = SMBus(1)
# Register addresses (with "normal mode" power-down bits)
reg_write_dac = 0x40
address = 0x60
voltage = 0xaaa

msg = (voltage & 0xff0) >> 4
msg = [msg, (msg & 0xf) << 4]

bus.write_i2c_block_data(address, reg_write_dac, msg)