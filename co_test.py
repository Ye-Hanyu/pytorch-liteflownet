import serial
import time

if __name__ == '__main__':
    ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)  # dmesg | grep tty 查看端口
    print(ser)
    ser.close()
    ser.open()
    print(ser.isOpen())
    if ser.isOpen():
        print("open success")
    else:
        print("open failed")
    while True:
        hex_str = bytes.fromhex('01 03 00 12 00 01 24 0F')
        ser.write(hex_str)
        res = ser.readall()
        temp = res.hex()
        print("16进制源数据:", temp)
        d1 = temp[6:10]
        d1 = int(d1, 16)
        d1 = float(d1)/10
        print("10进制数据是:", d1)
        time.sleep(1)
ser.close()
