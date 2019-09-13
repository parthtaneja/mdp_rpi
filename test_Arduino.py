from module.Serial import *

if __name__ == '__main__':
    serial = Serial()
    serial.connect()
    print("[@] Arduino connection successfully established")
    try:
        msg = input("Enter msg to send: ")
        print("[@] Writing to Arduino: {}".format(msg))
        serial.write(msg)
        msg = serial.read()
        print("[@] Got from Arduino: {}".format(msg))
        print("[@] Closing socket.")
        # serial.close()
    except Exception as e:
        print(e)