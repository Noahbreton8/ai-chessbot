class Piece():
    def __init__(self, game, row, col, identifier):
        self.row = row
        self.col = col
        self.identity = identifier
        self.colour = identifier[0]
        self.image = game.transform.scale(game.image.load("images/"+identifier+".png"), (100, 100))
    
    def draw(self, game, screen, size):
        screen.blit(self.image, game.Rect(self.col*size, self.row*size, size, size))

    def moveTo(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return self.identity