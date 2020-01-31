import socket
import select
from threading import Thread

class GameSocket:
    def connect_to_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 25565))
        return s

    def __init__(self):
        self.socket = self.connect_to_server()
        self.Listener = Listener(self.socket)
        self.Listener.start()

    def close(self):
        print('Closing connection to server')
        self.Listener.running = False
        self.socket.close()

class Listener(Thread):
    def __init__(self, socket):
        super().__init__()
        self.socket = socket
        self.running = True

    def run(self):
        while self.running:
            ready = select.select([self.socket], [], [], 0.05)
            if ready[0]:
                data = self.socket.rev(1024).decode()
                print(data, flush = True)
