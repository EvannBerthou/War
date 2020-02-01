import socket
import curses
import select
from threading import Thread

class ClientThread(Thread):
    def __init__(self, ip, port, socket, server):
        super().__init__()
        self.ip, self.port = ip, port
        self.identifier = f'{ip}:{port}'
        self.socket = socket
        self.running = True
        self.server = server

    def run(self):
        while self.running:
            ready = select.select([self.socket], [], [], 0.05)
            if ready[0]:
                r = self.socket.recv(1024).decode()
                if r.strip(' ') != "":
                    self.server.add_str(r)
                else:
                    self.server.add_str('[-] Déconnexion d\'un joueur')
                    server.clients.remove(self)
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

        self.clients = []

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
                self.add_str('[+] Nouvelle connection.')
                newthread = ClientThread(ip, port, socket, self)
                newthread.start()
                self.clients.append(newthread)
                clients = self.get_client_list()
                for client in self.clients:
                    client.socket.send(f'clients {clients}'.encode())

    def get_client_list(self):
        return " ".join([client.identifier for client in self.clients])

server = Server()
server.run()
