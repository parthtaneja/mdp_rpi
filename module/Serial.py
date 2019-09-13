import serial
import time


class Serial:
    def __init__(self):
        self.port = "/dev/ttyACM0"
        self.baud_rate = 115200
        self.serial = None

    def connect(self):
        try:
            print ("[@] Connecting to Serial..")
            self.serial = serial.Serial(self.port, self.baud_rate)
            time.sleep(3)
            print("[@] Serial link is connected")
        except Exception as e:
            print("[!] Unable to connect serial link.")
            print(e)

    def close(self):
        if self.serial != None:
            self.serial.close()
        print("[@] Serial link is now closed")

    def write(self, msg):
        try:
            return self.serial.write(msg)
        except Exception as e:
            print("[!] Error writing to serial link")
            print(e)

    def read(self):
        # https://pythonhosted.org/pyserial/shortintro.html#readline
        try:
            return self.serial.readline()
        except Exception as e:
            print("[!] Error reading from serial link")
            print(e)
