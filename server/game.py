from board import Board
from round import Round
from random import *


class Game(object):
    def __init__(self, id, players):
        self.id = id
        self.players = players
        self.words_used = set()
        self.round = None
        self.board = Board()
        self.player_draw_ind = 0
        #self.connected_thread = thread
        self.round_count = 1
        self.start_new_round()

    def start_new_round(self):
        # inicia um round com palavra
        try:
            round_word = self.get_word()
            self.round = Round(
                round_word, self.players[self.player_draw_ind], self)
            # self.player_draw_ind += 1
            self.round_count += 1

            if (self.player_draw_ind >= len(self.players)):
                self.round_ended()
                self.end_game()
            self.player_draw_ind += 1
        except Exception as e:
            self.end_game()

    def create_board(self):
        # creates a blank board
        self.board = Board()

    def player_guess(self, player, guess):
        #    permite que o jogador  adivinhe a palavra
        return self.round.guess(player, guess)

    def player_disconnected(self, player):
        # limpa os objetos quando o jogador sai
        if player in self.players:
            player_ind = self.players.index(player)
            if player_ind >= self.player_draw_ind:
                self.player_draw_ind -= 1
            self.players.remove(player)
            self.round.player_left()
        else:
            raise Exception("Player not in the game ")
        if len(self.players < 2):
            self.end_game()

    def get_player_scores(self):  # retorna um dicionario com a pontuação dos jogadores
        scores = {player: player.get_score() for player in self.players}
        return scores

    def skip(self):
        # Incrementa os rounds
        if (self.round):
            new_round = self.round.skip()
            if new_round:
                self.round_ended()
                return True
            return False
        else:
            raise Exception("Nenhum round iniciado!")
        pass

    def round_ended(self):
        # If the round ends call this, reset round
        self.round.skips = 0
        self.start_new_round()
        self.board.clear()
        pass

    def update_board(self, x, y, color):
        # calls update method on board
        if not self.board:
            raise Exception("Sem board ainda")
        self.board.update(x, y, color)

    def end_game(self):
        print(f"[GAME] Game {self.id} ended")
        for player in self.players:
            player.game = None
        

    def get_word(self):
        with open("words.txt", "r")as f:
            words = []
            for line in f:

                wrd = line.strip()
                if wrd not in self.words_used:
                    words.append(wrd)
            self.words_used.add(wrd)
            r = random.randint(0, len(words))
            return words[r].strip()
