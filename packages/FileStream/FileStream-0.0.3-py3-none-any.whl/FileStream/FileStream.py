import socket
import os
from EasyCode.EasyCode import getPath

class _receive_str:
    FILE = None
    EXT = None
    IP = socket.gethostbyname(socket.gethostname())
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def receive_connection(self, ip, port):
        self.client.connect((ip, port))
    def receive(self):
        filename = self.client.recv(1024).decode("utf-8")
        self.FILE = filename.split(".")[0]
        self.EXT = filename.split(".")[-1]
        file = open("Unknow.fs", 'wb')
        data = self.client.recv(1024)
        while True:
            if not data:
                break
            file.write(data)
            data = self.client.recv(1024)
    def save(self, file="", ext=""):
        if file!="" and ext!="":
            os.rename("Unknow.fs", f'{file}.{ext}')
        elif file=="" and ext=="":
            os.rename("Unknow.fs", f"{self.FILE}.{self.EXT}")
        else:
            raise Exception(f"{str} expected found {type(file)} {type(ext)}")


class _send:
    IP = socket.gethostbyname(socket.gethostname())
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def bind_server(self, ip, port):
        self.server.bind((ip, port))
    def accept_connection(self):
        self.server.listen()
        self.client, address = self.server.accept()
    def send(self, filename, tkinter_path=False, rate=1024):
        try:
            if tkinter_path:
                self.client.send(getPath(filename).split("/")[-1].encode('utf-8'))
                file = open(getPath(filename), 'rb')
            else:
                self.client.send(filename.encode('utf-8'))
                file = open(filename, 'rb')
            data = file.read(rate)
            while data:
                self.client.send(data)
                data = file.read(rate)
            return True
        except:
            return False
    def close_connection_securly(self):
        self.client.close()
        self.server.close()
class Send_Stream(_send):
    def __init__(self, addr, filename, tkinter_path=False, Intimation=""):
        super().__init__()
        self.ip, self.port = addr
        self.bind_server(self.ip, self.port)
        print(Intimation)
        self.accept_connection()
        self.send(filename, tkinter_path=tkinter_path, rate=1024)
    def close_connections(self):
        self.close_connection_securly()



class Receive(_receive_str):
    def __init__(self, addr):
        super().__init__()
        self.ip, self.port = addr
        self.receive_connection(self.ip, self.port)
        self.receive()
    def save_file(self, filename=""):
        FILE = ""
        EXT  = ""
        if "." not in filename and filename!="" and filename==".":
            raise Exception("File name is inappropriate")
        else:
            FILE = filename.split(".")[0]
            EXT = filename.split(".")[-1]
        self.save(FILE, EXT)


