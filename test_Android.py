from module.Android import *

if __name__ == "__main__":
    android = Android(bluetooth_channel = 3)
    android.connect()
    print("[@] Bluetooth connection successfully established")
    try:
        msg = input("Enter msg to send: ")
        print("[@] Writing to Bluetooth: {}".format(msg))
        android.write(msg)
        msg = android.read()
        print("[@] Got from Bluetooth: {}".format(msg))
        print("[@] Closing socket.")
        android.close()
    except Exception as e:
        print(e)
