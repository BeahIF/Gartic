import pygame

class Chat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.WIDTH = 300
        self.HEIGHT = 800
        self.BORDER_THICKNESS = 5
        self.content = []
        self.typing = ""
        
    def update_chat(self, msg):
        self.content.append(msg)
        
    def draw(self, win):
        pygame.draw.rect(win, (0,0,0),(self.x,self.y,self.WIDTH,self.HEIGHT), self.BORDER_THICKNESS)
        
    def type(self, char):pass