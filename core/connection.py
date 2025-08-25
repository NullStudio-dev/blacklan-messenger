import socket
import json

class Connection:
    def __init__(self, host, port, buffer_size):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send(self, data):
        self.socket.sendall(json.dumps(data).encode("utf-8"))

    def receive(self):
        return json.loads(self.socket.recv(self.buffer_size).decode("utf-8"))

    def close(self):
        self.socket.close()


