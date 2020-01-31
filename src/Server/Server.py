import socket
import curses
import select
from threading import Thread

class ClientThread(Thread):
    def __init__(self, ip, port, socket):
        super().__init__()
        self.ip, self.port = ip, port
        self.socket = socket
        self.running = True

    def run(self):
        while self.running:
            ready = select.select([self.socket], [], [], 0.05)
            if ready[0]:
                r = self.socket.recv(1024).decode()
                if r.strip(' ') != "":
                    print(r)
                else:
                    self.running = False

class Server:
    def create_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', self.port))
        return s

    def __init__(self):
        self.port = 25565
        self.socket = self.create_socket()
        self.running = True

        self.stdscr = curses.initscr()
        self.size = self.stdscr.getmaxyx()
        self.current_row = 0
        self.stdscr.scrollok(True)

    def add_str(self, text):
        self.stdscr.addstr(f'{text}\n')
        self.current_row += 1
        self.stdscr.refresh()

    def run(self):
        self.add_str("[+] Démarrage du Server.")
        while self.running:
            self.socket.listen(5)
            connexions, wlist, xlist = select.select([self.socket], [], [], 0.05)

            for connexion in connexions:
                (socket, (ip, port)) = self.socket.accept()
                self.add_str('nouvelle connexion')
                newthread = ClientThread(ip, port, socket)
                newthread.start()

server = Server()
server.run()
