import socket
import curses
import select
import json
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
                    parts = r.split(' ')
                    if parts[0] == "targets":
                        self.server.actions[self.identifier] = ['targets', parts[1:]]
                    if parts[0] == "defense":
                        self.server.actions[self.identifier] = ['defense']
                    self.server.confirm_actions()
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

        self.actions = {}
        self.scores = {}

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
                self.scores[f'{ip}:{port}'] = 0
                clients = self.get_client_list()
                for client in self.clients:
                    client.socket.send(f'clients {clients}'.encode())

    def get_client_list(self):
        return " ".join([client.identifier for client in self.clients])

    def confirm_actions(self):
        self.add_str(self.actions)
        if len(self.actions) == len(self.clients):
            self.add_str('Fin du tour')
            self.end_turn()

    def end_turn(self):
        for player in self.actions:
            action = self.actions[player]
            if action[0] == 'targets':
                targets = [target for target in action[1]]
                for target in targets:
                    ennemy_action = self.actions[target][0]
                    if ennemy_action == 'targets':
                        self.scores[player] += 10
                        self.scores[target] -= 10

                    if ennemy_action == 'defense':
                        self.scores[target] += 10
                        self.scores[player] -= 10

            if action[0] == 'defense':
                self.scores[player] -= len(self.clients) - 1
                for key in self.scores:
                    if key != player:
                        self.scores[key] += 1

        self.add_str(self.scores)
        self.send_score()

    def send_score(self):
        str_data = json.dumps(self.scores)
        for client in self.clients:
            client.socket.send(('scores ' + str_data).encode())

server = Server()
server.run()
