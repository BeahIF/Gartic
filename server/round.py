import time
from _thread import *
import time as t
from _thread import *
# from game import Game
from chat import Chat
import threading


class Round(object):
    def __init__(self, word, player_drawing, game):
        # param word:str
        # param player_Drawing : Player
        # param players: Player[]
        self.word = word
        self.player_drawing = player_drawing
        self.player_guessed = []
        self.players_skipped = []
        self.skips = 0
        self.time = 75
        self.game = game
        self.player_scores = {player: 0 for player in self.game.players}
        # self.start = time.time()
        self.chat = Chat(self)
        # threading.Timer(1, self.time_thread)
        start_new_thread(self.time_thread, ())

    def skip(self, player):
        if player not in self.players_skipped:
            self.chat.update_chat(
                f"Jogador votou para pular ({self.skips}/{len(self.players)-2})")
            self.players_skipped.append(player)
            self.skips += 1
            if self.skips > len(self.game.players)-2:
                # self.skips = 0
                return True
        return False

    def get_scores(self):

        # returns all the players scores
        return self.player_scores

    def get_score(self, player):
        # get a specific player score
        if player in self.player_scores:
            return self.player_scores[player]
        else:
            raise Exception("Player not in score list")

    def time_thread(self):
        # gerencia do tempo
        while self.time > 0:
            t.sleep(1)
            self.time -= 1
        self.end_round("tempo acabou")

    def guess(self, player, wrd):
        # returns bool if player got guess correct
        # param player:Player
        # param word:string
        # return bool
        correct = wrd == self.word
        if (correct):
            self.player_guessed.append(correct)
            # TODO implementar o sistema de score
            self.chat.update_chat(f"{player.name} has guessed the word.")
            return True

        self.chat.update_chat(f"{player.name} guessed {wrd}")
        return False

    def player_left(self, player):
        # removes player that left from scores and
        # param player : Player
        # return: None
        if player in self.player_scores:
            del self.player_scores[player]
        if player in self.player_guessed:
            self.player_guessed.remove(player)
        if player == self.player_drawing:
            self.chat.update_chat(
                f"Round has been skipped becouse the drawer left.")
            self.end_round("Tempo da rodada acabou ")

    def end_round(self, msg):
        for player in self.game.players:
            if player in self.player_scores:
                player.update_score(self.player_scores[player])
        self.game.round_ended()
