from leaderboard import Leaderboard
from player import Player
from top_bar import TopBar
import pygame
from button import *
from board import *
from bottom_bar import BottomBar
from chat import Chat
from network import Network


class Game:
    BG = (255, 255, 255)
    COLORS = {

        (255, 255, 255): 0,  # white
        (0, 0, 0): 1,       # black
        (255, 0, 0): 2,     # red
        (0, 255, 0): 3,     # green
        (0, 0, 255): 4,     # blue
        (255, 255, 0): 5,   # yellow
        (255, 140, 0): 6,   # orange
        (165, 42, 42): 7,   # brown
        (128, 0, 128): 8    # purple

    }

    def __init__(self, win, connection=None):
        pygame.font.init()
        self.connection = connection
        self.win = win
        # self.width = 1000
        # self.height = 600
        # self.win = pygame.display.set_mode((self.width, self.height))
        self.leaderboard = Leaderboard(50, 110)
        self.board = Board(305, 110)
        self.top_bar = TopBar(10, 10, 1280, 100)
        self.top_bar.change_round(1)
        self.players = []
        self.skip_button = TextButton(85, 830, 125, 60, (255, 255, 0), "Skip")
        self.bottom_bar = BottomBar(305, 880, self)
        self.chat = Chat(1000, 125)
        # self.drawingPlayer = False
        self.draw_color = (0, 0, 0)
        for player in self.players:
            self.leaderboard.add_player(player)

    def add_player(self, player):
        self.players.append(player)
        self.leaderboard.add_player(player)

    def draw(self):
        self.win.fill(self.BG)
        self.leaderboard.draw(self.win)
        self.top_bar.draw(self.win)
        self.board.draw(self.win)
        self.skip_button.draw(self.win)
        self.bottom_bar.draw(self.win)
        pygame.display.update()

    def check_clicks(self):
        mouse = pygame.mouse.get_pos()
        if self.skip_button.click(*mouse):
            print("Clicked o botao pular")
            skips = self.connection.send({1: []})
        clicked_board = self.board.click(*mouse)
        if clicked_board:
            self.board.update(*clicked_board, self.draw_color)
            self.connection.send(
                {8: [*clicked_board, self.COLORS[tuple(self.draw_color)]]})

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            try:
                response = self.connection.send({3: []})
                self.board.compressed_board = response
                self.board.translate_board()
                response = self.connection.send({9: []})
                self.top_bar.time = response
                response = self.connection.send({2: {}})
                self.chat.update_chat(response)
                if not self.top_bar.word:
                    self.top_bar.word = self.connection.send({6: []})
                # response = self.connection.send({0: []})
                # self.players = []
                # for player in response:
                #     p = Player(player)
                #     self.add_player(p)

            except:
                run = False
                break
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                # if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    self.check_clicks()
                    self.bottom_bar.button_events()
                if event.type in pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.chat.update_chat()
                        self.connection.send({0: [self.chat.typing]})
                        self.chat.typing = ""
                    else:

                        key_name = pygame.key.name(event.key)
                        key_name = key_name.lower()
                        self.chat.type(key_name)
        pygame.quit()


# if __name__ == "__main__":
#     pygame.font.init()
#     g = Game()
#     g.run()
