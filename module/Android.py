from bluetooth import *
import os


class Android:
    def __init__(self):
        self.server_socket = None
        self.client_socket = None
        self._is_connected = False

    def close(self):
        if self.client_socket != None:
            print("[!] Android: closing bluetooth socket")
            self.client_socket.close()
        if self.server_socket != None:
            print("[!] Android: closing server socket")
            self.server_socket.close()
        self._is_connected = False

    def is_connected(self):
        return self._is_connected

    def connect(self):
        bluetooth_port = 4
        try:
            self.server_socket = BluetoothSocket(RFCOMM)
            self.server_socket.bind(("", bluetooth_port))
            self.server_socket.listen(1)
            self.port = self.server_socket.getsockname()[1]
            uuid = "00001101-0000-1000-8000-00805F9B34FB"
            advertise_service(
                self.server_socket,
                "MDP22",
                service_id=uuid,
                service_classes=[uuid, SERIAL_PORT_CLASS],
                profiles=[SERIAL_PORT_PROFILE],)
            print("Waiting for connection on RFCOMM channel on port {}".format(self.port))
            self.client_socket, client_address = self.server_socket.accept()
            print("[@] Accepted connection from {}".format(client_address))
            self._is_connected = True
        except Exception as e:
            print(e)

    def write(self, msg):
        try:
            self.client_socket.send(str(msg))
        except Exception as e:
            print("[!] Error writing message to BT device.")
            print(e)

    def read(self):
        try:
            return self.client_socket.recv(2048)
        except Exception as e:
            print("[!] Error reading message from BT device. Reconnecting..")
            self.connect()
