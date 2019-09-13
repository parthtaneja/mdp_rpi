from module.Serial import *
from module.Android import *
import time

if __name__ == '__main__':
    android = Android()
    android.connect()
    print("[@] Bluetooth connection successfully established")
    serial = Serial()
    serial.connect()
    print("[@] Arduino connection successfully established")
    while True:
        msg = android.read()
        print("[@] Got from Android: {}".format(msg))
        print("[@] Writing to Arduino: {}".format(msg))
        serial.write(msg)
        time.sleep(3)