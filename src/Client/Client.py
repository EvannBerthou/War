import socket
import select
from threading import Thread

class GameSocket:
    def connect_to_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.connect(('192.168.1.41', 25565))
        s.connect(('127.0.0.1', 25565))
        return s

    def __init__(self, game):
        self.socket = self.connect_to_server()
        self.port = self.socket.getsockname()[1]
        self.Listener = Listener(self.socket, game)
        self.Listener.start()

    def close(self):
        print('Closing connection to server')
        self.Listener.running = False
        self.socket.close()

class Listener(Thread):
    def __init__(self, socket, game):
        super().__init__()
        self.socket = socket
        self.game = game
        self.running = True

    def run(self):
        while self.running:
            ready = select.select([self.socket], [], [], 0.05)
            if ready[0]:
                data = self.socket.recv(1024).decode()
                print(data, flush = True)
                parts = data.split(' ')
                if parts[0] == 'clients':
                    client_list = parts[1:]
                    self.game.add_player(client_list)
