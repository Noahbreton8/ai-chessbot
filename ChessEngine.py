from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.queen import Queen

class GameState():
    def __init__(self, game):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.board[7][0] = Rook(game, 7, 0, 'wR')
        self.board[7][7] = Rook(game, 7, 7, 'wR')
        self.board[7][1] = Knight(game, 7, 1, 'wN')
        self.board[7][6] = Knight(game, 7, 6, 'wN')
        self.board[7][2] = Bishop(game, 7, 2, 'wB')
        self.board[7][5] = Bishop(game, 7, 5, 'wB')
        self.board[7][3] = Queen(game, 7, 3, 'wQ')
        self.board[7][4] = King(game, 7, 4, 'wK')

        self.board[0][0] = Rook(game, 0, 0, 'bR')
        self.board[0][7] = Rook(game, 0, 7, 'bR')
        self.board[0][1] = Knight(game, 0, 1, 'bN')
        self.board[0][6] = Knight(game, 0, 6, 'bN')
        self.board[0][2] = Bishop(game, 0, 2, 'bB')
        self.board[0][5] = Bishop(game, 0, 5, 'bB')
        self.board[0][3] = Queen(game, 0, 3, 'bQ')
        self.board[0][4] = King(game, 0, 4, 'bK')

        for i in range(8):
            self.board[6][i] = Pawn(game, 6, i, 'wP')
            self.board[1][i] = Pawn(game, 1, i, 'bP')


