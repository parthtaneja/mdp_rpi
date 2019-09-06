import socket
import os


class PC():
    def __init__(self):
        self.tcp_ip = "192.168.1.1"
        self.port = 5182
        self.connection = None
        self.client = None
        self.address = None
        self._is_pc_connected = False

    def is_connected(self):
        return self._is_pc_connected

    def close(self):
        if self.connection != None:
            self.connection.close()
        if self.client != None:
            self.client.close()
        self._is_pc_connected = False

    def connect(self):
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.bind((self.tcp_ip, self.port))
            self.connection.listen(1)
            print ("[@] Listening for incoming connections from PC...")
            self.client, self.address = self.connection.accept()
            print ("[@] Connected! Connection address: {}").format(self.address)
            self._is_pc_connected = True
        except Exception as e:
            print ("[!] Error connecting to PC")
            print (e)
        
    def write(self, msg):
        try:
            self.client.sendto(msg, self.address)
        except Exception as e:
            print ("[!] Error writing message")
            print (e)

    def read(self):
        try:
            return self.client.recv(2048)
        except Exception as e:
            print ("[!] Error reading message")
            print (e) 