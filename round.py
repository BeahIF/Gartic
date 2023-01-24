import time
from _thread import *
import time as t
from _thread import *

from chat import Chat


class Round(object):
    def __init__(self, word, player_drawing, game):
        # param word:str
        # param player_Drawing : Player
        # param players: Player[]
        self.word = word
        self.player_drawing = player_drawing
        self.player_guessed = []
        self.skips = 0
        self.game = game
        self.player_scores = {player: 0 for player in self.game.players}
        self.time = 75
        self.start = time.time()
        self.chat = Chat(self)
        start_new_thread(self.time_thread, ())

    def skip(self):
        self.skips += 1
        if self.skips > len(self.players)-2:
            self.skips = 0
            return True
        return False

    def get_scores(self):

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

    def player_left(self, player):
        # removes player that left from scores and
        # param player : Player
        # return: None
        if player in self.player_scores:
            del self.player_scores[player]
        if player in self.player_guessed:
            self.player_guessed.remove(player)
        if player == self.player_drawing:
            self.end_round("Tempo da rodada acabou ")

    def end_round(self, msg):
        pass
