

class Board(object):
    ROWS = COLS = 720
    COLORS = {
        
        0: (255,255,255), # white
        1: (0,0,0),       # black
        2: (255,0,0),     # red
        3: (0,255,000),   # green
        4: (0,0,255),     # blue
        5: (255,255,0),   # yellow
        6: (255,140,0),   # orange
        7: (165,42,42),   # brown
        8: (128,0,128)    # purple
        
    }
        
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.compressed_board = []
        self.board = [[(255,255,255) for _ in range(self.COLS) for _ in range(self.ROWS)]]
    
    def draw(self, win):
        pass
    
    def click(self, x, y):
        pass
    
    def update(self, x, y, color):
        pass
    
    def clear(self):
        pass
    