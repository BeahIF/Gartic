import socket
import threading
from player import Player
from game import Game
import json


class Server(object):
    PLAYERS = 2

    def __init__(self):
        self.connection_queue = []
        self.game_id = 0

    def player_thread(self, conn,  player):
        # faz a comunicação entre os clientes
        while True:
            try:
                # send_msg =
                # receive request
                try:
                    data = conn.recv(1024)
                    data = json.loads(data.decode())
                    print("[LOG] Recived data:", data)
                except Exception as e:
                    break
                
                # keys = [key for key in data.split()]
                # keys = [int(data[0])]
                keys = [int(key) for key in data.keys()]
                send_msg = {key: [] for key in keys}

                for key in keys:
                    if key == -1:  # get game, retorna uma lista de jogadores
                        if player.game:
                            send = {player.get_name(): player.get_score()
                                    for player in player.game.players}
                            send_msg[-1] = send
                        else:
                            send_msg[-1] = []
                    if player.game:
                        if key == 0:  # guess
                            correct = player.game.player_guess(
                                player, data['0'][0])
                            send_msg[0] = correct
                        elif key == 1:  # skip
                            skip = player.game.skip()
                            send_msg[1] = skip
                        elif key == 2:  # get chat
                            content = player.game.round.chat.get_chat()
                            send_msg[2] = content
                        elif key == 3:  # get board
                            brd = player.game.board.get_board()
                            send_msg[3] = brd
                        elif key == 4:  # get score
                            scores = player.game.get_player_scores()
                            send_msg[4] = scores
                        elif key == 5:  # get round
                            rnd = player.game.round.round_count
                            send_msg[5] = rnd
                        elif key == 6:  # get word
                            word = player.game.round.word
                            send_msg[6] = word
                        elif key == 7:  # get skips
                            skips = player.game.round.skips
                            send_msg[7] = skips
                        elif key == 8:  # update board
                            x, y, color = data[8][:3]
                            self.game.update_board(x, y, color)
                        elif key == 9:  # get round time
                            t = self.game.round.time
                            send_msg[9] = t
                    # if key == 10:
                    #     raise Exception("Not valid request")
                send_msg = json.dumps(send_msg)
                conn.sendall(send_msg.encode() + ".".encode())
                
            except Exception() as e:

                print(f"Exception{player.get_name()} disconected:", e)
                break
                
        #player.game.player_disconnected(player)
        conn.close()

    def handle_queue(self, player):
        self.connection_queue.append(player)
        if len(self.connection_queue) >= 2:
            game = Game(self.game_id, self.connection_queue[:],)
            for p in self.connection_queue:
                p.set_game(game)
            self.game_id += 1

            self.connection_queue = []

    def authentication(self, conn, addr):
        try:
            data = conn.recv(1024)
            name = str(data.decode())
            if not name:
                raise Exception("No name received")
            conn.sendall("1".encode())
            player = Player(addr, name)
            self.handle_queue(player)
            thread = threading.Thread(
                target=self.player_thread, args=(conn, player))
            thread.start()
        except Exception as e:
            print("Exceprion", e)
            # self.client.shutdown(socket.SHUT_RDWR)
            conn.close()
        # thread = threading.Thread(
        #     target=self.player_thread, args=(conn, addr))
        # thread.start()

    def connection_thread(self):
        server = "localhost"
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
            self.authentication(conn, addr)


if __name__ == "__main__":
    s = Server()
    thread = threading.Thread(target=s.connection_thread())
    thread.start()
