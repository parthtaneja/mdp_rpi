import sys
import time
import queue as queue
import threading
from module.Android import *
from module.PC import *
from module.Serial import *


class Main:
    def __init__(self):
        threading.Thread.__init__(self)

        self.pc = PC()
        self.android = Android()
        self.serial = Serial()

        self.pc.connect()
        self.android.connect()
        self.serial.connect()

        self.pc_queue = queue.Queue(maxsize=0)
        self.android_queue = queue.Queue(maxsize=0)
        self.serial_queue = queue.Queue(maxsize=0)
        time.sleep(1)

    def write_to_pc(self, pc_queue):
        print("[@] Attempting write_to_pc..")
        while True:
            if not pc_queue.empty():
                msg = pc_queue.get_nowait()
                self.pc.write(msg)
                print("[@] Sent to PC: {}").format(msg)

    def read_from_pc(self, android_queue, serial_queue):
        print("[@] Reading from PC connection..")
        while True:
            msg = self.pc.read()
            initial = msg[0].lower()
            if initial == "a":
                android_queue.put_nowait(msg[1:])
                print("[@] Received from PC to Android: {}").format(msg)
            elif initial == "h":
                serial_queue.put_nowait(msg[1:])
                print("[@] Received from PC to Serial: {}").format(msg)
            else:
                print("[!] Incorrect header received from PC: {}").format(initial)
                time.sleep(1)

    def write_to_android(self, android_queue):
        print("[@] Attempting write_to_android..")
        while True:
            if not android_queue.empty():
                msg = android_queue.get_nowait()
                self.android.write(msg)
                print("[@] Sent to Android: {}").format(msg)

    def read_from_android(self, pc_queue, serial_queue):
        while True:
            msg = self.android.read()
            initial = msg[0].lower()
            if initial == "p":
                pc_queue.put_nowait(msg[1:])
                print("[@] Received from Android to PC: {}").format(msg)
            elif initial == "a":
                serial_queue.put_nowait(msg[1:])
                print("[@] Received from Android to Arduino: {}").format(msg)
            elif initial == "x":
                serial_queue.put_nowait(msg[1:])
                pc_queue.put_nowait(msg[1:])
                print("[@] Received from Android to Arduino & PC: {}").format(msg)
            else:
                print("[!] Incorrect header received from Android: {}").format(
                    initial)
                time.sleep(1)

    def write_to_serial(self, serial_queue):
        print("[@] Attempting write_to_serial..")
        while True:
            if not serial_queue.empty():
                msg = serial_queue.get_nowait()
                self.serial.write(msg)
                print("[@] Sent to Serial: {}").format(msg)

    def read_from_serial(self, pc_queue, android_queue):
        while True:
            msg = self.serial.read()
            initial = msg[0].lower()
            if initial == "p":
                pc_queue.put_nowait(msg[1:])
                print("[@] Received from Arduino to PC: {}").format(msg)
            elif initial == "b":
                android_queue.put_nowait(msg[1:])
                print("[@] Received from Arduino to Android: {}").format(msg)
            else:
                print("[!] Incorrect header received from Android: {}").format(
                    initial)
                time.sleep(1)

    def keep_alive(self):
        while True:
            time.sleep(1)

    def initialise_threads(self):
        read_pc = threading.Thread(target=self.read_from_pc, args=(
            self.android_queue, self.serial_queue), name="pc_read_thread")
        write_pc = threading.Thread(target=self.write_to_pc, args=(
            self.pc_queue,), name="pc_write_thread")

        read_android = threading.Thread(target=self.read_from_android, args=(
            self.pc_queue, self.serial_queue), name="android_read_thread")
        write_android = threading.Thread(target=self.write_to_android, args=(
            self.android_queue,), name="android_write_thread")

        read_serial = threading.Thread(target=self.read_from_serial, args=(
            self.pc_queue, self.android_queue), name="serial_read_thread")
        write_serial = threading.Thread(target=self.write_to_serial, args=(
            self.serial_queue,), name="serial_write_thread")

        read_pc.daemon = True
        write_pc.daemon = True

        read_android.daemon = True
        write_android.daemon = True

        read_serial.daemon = True
        write_serial.daemon = True

        read_pc.start()
        write_pc.start()

        read_android.start()
        write_android.start()

        read_serial.start()
        write_serial.start()

    def close_all_connections(self):
        self.pc.close()
        self.android.close()
        self.serial.close()


if __name__ == "__main__":
    print("[@] Starting main program..")
    app = Main()
    try:
        app.initialise_threads()
        app.keep_alive()
    except Exception as e:
        print("[@] Error running main")
        app.close_all_connections()
        print(e)
