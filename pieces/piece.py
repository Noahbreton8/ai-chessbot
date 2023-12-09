class Piece():
    def __init__(self, game, row, col, colour):
        self.row = row
        self.col = col
        self.image = game.image.load("images/"+colour+".png")
    
    def draw(self, game, screen, size):
        screen.blit(self.image, game.Rect(self.col*size, self.row*size, size, size))