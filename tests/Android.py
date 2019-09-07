from ..module.Android import *

if __name__ == "__main__":
    android = Android()
    android.connect()
    print("[@] Bluetooth connection successfully established")
    try:
        msg = raw_input()
        print("[@] Writing to Bluetooth: {}".format(msg))
        android.write(msg)
        msg = android.read()
        print("[@] Got from Bluetooth: {}".format(msg))
        print("Closing socket.")
        andorid.close()
    except Exception as e:
        print(e)
