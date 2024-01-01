import pygame as game
from ChessEngine import GameState
from ChessEngine import Move
import AiMoveGenerator

HEIGHT = WIDTH = 800
SIZE = WIDTH, HEIGHT
DIMENTION = 8
SQUARE_SIZE = WIDTH/DIMENTION

'''
Handles what needs to happen during the game
'''
def main():
    game.init()
    screen = game.display.set_mode(SIZE)
    screen.fill((255, 255, 255))

    #Initialize game
    gs = GameState(game)
    
    #Draw initial screen
    drawGameState(screen, gs) 

    #Starting moves
    validMoves = gs.getValidMoves()
    moveMade = False #until valid move is made don't regenerate validMoves

    currSelection = () #keeps track of current choice
    playerMoves = [] #keeps track of at most 2 choices for moving pieces

    player1 = False #True if a human player, false if the AI plays
    player2 = False #Same as player 1

    gameOn = True
    while gameOn:
        humanTurn = (gs.whiteTurn and player1) or (not gs.whiteTurn and player2)
        for event in game.event.get():

            #Exit button is clicked
            if event.type == game.QUIT:
                gameOn = False
            
            #Selecting squares
            elif event.type == game.MOUSEBUTTONDOWN:
                if (not gs.checkmate and not gs.stalemate) and humanTurn:
                    x,y = game.mouse.get_pos()

                    #Turns mouse position into rank and file
                    col = int(x//SQUARE_SIZE)
                    row = int(y//SQUARE_SIZE)

                    #if we reselect a sqaure deselect it
                    if currSelection == (row, col):
                        currSelection = ()
                        playerMoves = []

                    else:
                        #if our first click is an empty square do nothing
                        if len(playerMoves) == 0 and gs.board[row][col] == None:
                            continue
                        
                        currSelection = (row, col)
                        playerMoves.append(currSelection)

                        #check if more than one click has been made
                        if len(playerMoves) == 2:
                            #check if second choice colour is same as first choice colour
                            if gs.board[playerMoves[1][0]][playerMoves[1][1]] and gs.board[playerMoves[0][0]][playerMoves[0][1]].colour == gs.board[playerMoves[1][0]][playerMoves[1][1]].colour:
                                playerMoves = playerMoves[1:] #remove the first move 

                            # second click is an opponent's piece or a empty square
                            else:
                                move = Move(playerMoves[0], playerMoves[1], gs.board)
                                print(move.getAlgebraicNotation())
                                for i in range(len(validMoves)):
                                    if move == validMoves[i]:
                                        moveMade = True

                                        #If its a pawn promotion ask the user what they want to promote to
                                        if validMoves[i].isPawnPromotion:
                                            # choice = input("Enter a promotion choice: \n \tFor Queen enter 'q'\n\tFor Rook enter 'r' \n\tFor Knight enter 'n' \n\tFor Bishop enter 'b'\n").upper()
                                            # while choice not in 'QRNB':
                                            #     choice = input("Enter a promotion choice: \n \tFor Queen enter 'q'\n\tFor Rook enter 'r' \n\tFor Knight enter 'n' \n\tFor Bishop enter 'b'\n").upper()
                                            choice = drawPieceSelection(screen)
                                            gs.movePiece(Move(playerMoves[0], playerMoves[1], gs.board, promotion=choice))
                                        else:
                                            gs.movePiece(validMoves[i])

                                        #reset selections
                                        currSelection = ()
                                        playerMoves = []
                                        break
                                
                            if not moveMade:
                                currSelection = ()
                                playerMoves = []
            
            #Undoing move
            elif event.type == game.KEYDOWN:
                if event.key == game.K_u:
                    gs.undoMove()
                    moveMade = True
        
        #AI move generation
        if (not gs.checkmate and not gs.stalemate) and not humanTurn:
            move = AiMoveGenerator.findBestMove(gs, validMoves)
            gs.movePiece(move)
            moveMade = True
        
        #If a move has been made regenerate valid moves
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        
        drawGameState(screen, gs, validMoves, currSelection)

        #End screen
        if gs.checkmate or gs.stalemate:
                result = drawEndScreen(screen, gs)
                if result == "Quit":
                    gameOn = False
                elif result == "Play Again":
                    gs = GameState(game)
                    drawGameState(screen, gs)
                    validMoves = gs.getValidMoves()
                    moveMade = False
                    currSelection = ()
                    playerMoves = []

        game.display.flip()

    game.quit()

'''
handles drawing everything on the screen
'''
def drawGameState(screen, gs, validMoves = [], sqSelected = ()):
    drawBoard(screen)
    highlightSqaures(screen, gs, validMoves, sqSelected)
    #highlightPieces(screen, gs)
    drawPieces(screen, gs)

'''
Draws the squares only
'''
def drawBoard(screen):
    colours = ((204, 183, 174), (112,102,119)) #((light colour), (dark colour)) feel free to change it
    for row in range(DIMENTION):
        for col in range(DIMENTION):
            #Drawing background colour
            colour = colours[(col+row) %2]
            game.draw.rect(screen, colour, game.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

'''
When a piece is selected, this draws what moves it can make and the piece selected
'''
def highlightSqaures(screen, gs, moves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c] != None and gs.board[r][c].colour == ('w' if gs.whiteTurn else 'b'):
            #highlight square
            s = game.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(game.Color('red'))
            screen.blit(s, (c*SQUARE_SIZE, r*SQUARE_SIZE))

            #highlight moves
            s.fill(game.Color('yellow'))
            for move in moves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQUARE_SIZE, move.endRow*SQUARE_SIZE))

'''
Draw just the piece image
'''
def drawPieces(screen, gs):
    for row in range(DIMENTION):
        for col in range(DIMENTION):
            #pieces draw themselves
            if gs.board[row][col] != None:
                gs.board[row][col].draw(game, screen, SQUARE_SIZE)

'''
Function for testing the white and black piece arrays
'''
def highlightPieces(screen, gs):
    whitePieces = gs.whitePieces
    blackPieces = gs.blackPieces
    for r, c in whitePieces:
        s = game.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(game.Color('purple'))
        screen.blit(s, (c*SQUARE_SIZE, r*SQUARE_SIZE))
    
    for r, c in blackPieces:
        s = game.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(game.Color('green'))
        screen.blit(s, (c*SQUARE_SIZE, r*SQUARE_SIZE))

'''
Drawing the endgame screen whether it's a checkmate or stalemate
'''
def drawEndScreen(screen, gs):
    font = game.font.Font(None, 74)
    message_font = game.font.Font(None, 36)
    endScreenDisplayed = True

    message = ""
    if gs.checkmate:
        message = "Checkmate!"
    elif gs.stalemate:
        message = "Stalemate!"

    options = ["Quit", "Play Again"]
    option_rects = []
    
    background_rect_padding = 30  # Adjusted padding
    text = font.render(message, True, game.Color("black"))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))

    for i, option in enumerate(options):
        option_text = message_font.render(option, True, game.Color("black"))
        option_rect = option_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
        option_rects.append((option, option_rect))

    #Calc dimensions for rectangle
    max_option_width = max(option_rect.width for _, option_rect in option_rects)
    background_rect_width = max_option_width + 2 * background_rect_padding
    background_rect_height = (text_rect.height + len(options) * 50 + 3 * background_rect_padding) // 2  # Reduced height
    background_rect_x = (WIDTH - max_option_width) // 2 - background_rect_padding
    background_rect_y = option_rects[0][1].top - background_rect_padding // 4 - 10# Adjusted vertical position

    #Draw the backgroynd of buttons
    background_rect = game.Rect(
        background_rect_x, background_rect_y, background_rect_width, background_rect_height
    )
    game.draw.rect(screen, (200, 200, 200), background_rect)

    while endScreenDisplayed:
        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                return "Quit"
            elif event.type == game.MOUSEBUTTONDOWN:
                x, y = game.mouse.get_pos()
                for option, option_rect in option_rects:
                    if option_rect.collidepoint(x, y):
                        if option == "Quit":
                            endScreenDisplayed = False  # Break the loop without quitting the game
                            return "Quit"
                        elif option == "Play Again":
                            endScreenDisplayed = False
                            return "Play Again"

        for option, option_rect in option_rects:
            screen.blit(
                message_font.render(option, True, game.Color("black")), option_rect
            )

        screen.blit(text, text_rect)

        game.display.flip()

    #To keep screen up
    return None

def drawButton(surface, text, position, size):
    font = game.font.Font(None, 36)
    button_text = font.render(text, True, game.Color("black"))
    button_rect = button_text.get_rect(center=(position[0] + size[0] // 2, position[1] + size[1] // 2))
    game.draw.rect(surface, (200, 200, 200), button_rect)
    surface.blit(button_text, button_rect)

def drawPieceSelection(screen):
    # Define even smaller overlay size and padding
    overlay_width = WIDTH // 6
    overlay_height = HEIGHT // 6
    overlay_padding = 5

     # Create an even smaller overlay surface
    overlay_surface = game.Surface((overlay_width, overlay_height), game.SRCALPHA)  # Use SRCALPHA for transparency

    # Draw brown border around the overlay
    border_rect = game.Rect((0, 0, overlay_width, overlay_height))
    game.draw.rect(overlay_surface, (139, 69, 19), border_rect, border_radius=5)

    # Draw white background inside the border
    background_rect = game.Rect((overlay_padding, overlay_padding, overlay_width - 2 * overlay_padding, overlay_height - 2 * overlay_padding))
    game.draw.rect(overlay_surface, (255, 255, 255), background_rect)

    # Draw images in a 2x2 grid on the even smaller overlay
    image_size = (overlay_width // 2 - overlay_padding * 2, overlay_height // 2 - overlay_padding * 2)
    image_positions = [
        (overlay_padding, overlay_padding),
        (overlay_width // 2 + overlay_padding, overlay_padding),
        (overlay_padding, overlay_height // 2 + overlay_padding),
        (overlay_width // 2 + overlay_padding, overlay_height // 2 + overlay_padding),
    ]

    image_names = ['wQ.png', 'wN.png', 'wR.png', 'wB.png']

    for name, position in zip(image_names, image_positions):
        drawImage(overlay_surface, name, position, image_size)

    overlay_x = (WIDTH - overlay_width) // 2
    overlay_y = (HEIGHT - overlay_height) // 2

    screen.blit(overlay_surface, (overlay_x, overlay_y))
    game.display.flip()

    while True:
        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                return None
            elif event.type == game.MOUSEBUTTONDOWN:
                x, y = game.mouse.get_pos()
                for i, position in enumerate(image_positions):
                    image_rect = game.Rect((position[0] + overlay_x, position[1] + overlay_y), image_size)
                    if image_rect.collidepoint(x, y):
                        return image_names[i][1]

def drawImage(surface, name, position, size):
    image = game.image.load(f'images/{name}')
    image = game.transform.scale(image, size)
    rect = image.get_rect(topleft=position)
    surface.blit(image, rect)

main()

#[[bR, bN, bB, bQ, bK, bB, bN, bR] <----8th rank (0th in the array)
# [bP, bP, bP, bP, bP, bP, bP, bP]
# []
# []
# []
# []
# [wP, wP, wP, wP, wP, wP, wP, wP]
# [wR, wN, wB, wQ, wK, wB, wK, wR]] <----1st rank (7th in the array)
#  ^                            ^
#  a file (0)                   h file (7)