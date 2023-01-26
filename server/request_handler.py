import socket
import threading
import time
from .player import Player
from .game import Game
from queue import Queue
import json


class Server(object):
    PLAYERS = 2

    def __init__(self):
        self.connection_queue = []
        self.game_id = 0

    def player_thread(conn, ip, name):
        # faz a comunicação entre os clientes
        while True:
            try:
                # send_msg =
                # receive request
                data = conn.recv(1024)
                data = json.loads(data)
                keys = [key for key in data.keys()]
                if key in keys:
                    if key == -1:

                    elif key == -1:
                    elif key == 0:
                    elif key == 2:
                    elif key == 3:
                    elif key == 4:
                    elif key == 5:

                    elif key == 6:
                    elif key == 7:
                    elif key == 8:
                    elif key == 9:
                    else:
                        raise Exception("Not valid request")

                conn.sendsall(json.dumps(send_msg))
            except Exception() as e:
                print(f"Exception{player.get_name()} disconected:", e)
                conn.close()

    def handle_queue(self, player):
        self.connection_queue.append(player)
        if len(self.connection_queue) >= 2:
            game = Game(self.connection_queue[:], self.game_id)
            for p in self.connection_queue:
                p.set_game(game)
            self.game_id += 1

            self.connection_queue = []

    def authentication(conn, addr):
        try:
            data = conn.recv(2048)
            name = str(data.decode())
            if not name:
                raise Exception("No name received")
            conn.sendall("1".encode())
        except Exception as e:
            print("Exceprion", e)
            conn.close()
        threading.Thread(target=self.player_thread, args=(conn, addr, name))

    def connection_thread():
        server = ""
        port = 5555

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((server, port))
        except socket.error as e:
            str(e)
        s.listen()
        print("Waiting for a connection, Server Started")
        while True:
            conn, addr = s.accept()
            print("New connection!")
            self.authentication(addr)

    if __name__ == "__main__":
        threading.Thread(target=connection_thread())
