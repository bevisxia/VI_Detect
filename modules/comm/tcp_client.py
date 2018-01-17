import socket
from libs.utils.decorator import except_caught

class TcpClient(object):
    def __init__(self, addr, port):
        self.__addr = addr
        self.__port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @except_caught
    def connect(self):
        self.__sock.connect((self.__addr, self.__port))

    @except_caught
    def reconnect(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    @except_caught
    def send(self, msg):
        self.__sock.sendall(msg)

    @except_caught
    def recv(self, len=1028):
        return self.__sock.recv(len)