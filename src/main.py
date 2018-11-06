import serial
ser = serial.Serial('/dev/ttyS0',115200)

print(ser)

while True:
    print(ser.readline().decode("utf-8"))