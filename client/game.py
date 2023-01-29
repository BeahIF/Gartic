from leaderboard import Leaderboard
from player import Player
from top_bar import TopBar
import pygame
from button import *
from board import *


class Game:
    BG = (255, 255, 255)

    def __init__(self):
        self.width = 1000
        self.height = 600
        self.win = pygame.display.set_mode((self.width, self.height))
        self.leaderboard = Leaderboard(50, 110)
        self.board = Board(305, 110)
        self.top_bar = TopBar(10, 10, 1280, 100)
        self.top_bar.change_round(1)
        self.players = [Player("Bea")]
        self.skip_button = TextButton(150, 450, 100, 50, (255, 255, 0), "Skip")
        # self.drawingPlayer = False
        for player in self.players:
            self.leaderboard.add_player(player)

    def draw(self):
        self.win.fill(self.BG)
        self.leaderboard.draw(self.win)
        self.top_bar.draw(self.win)
        self.board.draw(self.win)
        self.skip_button.draw(self.win)
        pygame.display.update()

    def check_clicks(self):
        mouse = pygame.mouse.get_pos()
        if self.skip_button.click(*mouse):
            print("Clicked o botao pular")
        clicked_board = self.board.click(*mouse)
        if clicked_board:
            self.board.update(*clicked_board, (0, 0, 0))

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                # if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    self.check_clicks()
        pygame.quit()


if __name__ == "__main__":
    pygame.font.init()
    g = Game()
    g.run()
