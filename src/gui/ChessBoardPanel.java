package gui;
import javax.swing.*;
import java.awt.*;

public class ChessBoardPanel extends JPanel {
    private static final int ROWS = 8;
    private static final int COLS = 8;
    private ChessPiece[][] pieces;

    public ChessBoardPanel() {
        pieces = new ChessPiece[ROWS][COLS];
        initializeChessBoard();
    }

    private void initializeChessBoard() {
        // Place pieces on the board
        pieces[0][0] = new Rook(0, 0);
        pieces[0][1] = new Knight(0, 1);
        pieces[0][2] = new Bishop(0, 2);
        pieces[0][3] = new Queen(0, 3);
        pieces[0][4] = new King(0, 4);
        pieces[0][5] = new Bishop(0, 5);
        pieces[0][6] = new Knight(0, 6);
        pieces[0][7] = new Rook(0, 7);

        pieces[7][0] = new Rook(7, 0);
        pieces[7][1] = new Knight(7, 1);
        pieces[7][2] = new Bishop(7, 2);
        pieces[7][3] = new Queen(7, 3);
        pieces[7][4] = new King(7, 4);
        pieces[7][5] = new Bishop(7, 5);
        pieces[7][6] = new Knight(7, 6);
        pieces[7][7] = new Rook(7, 7);

        for (int col = 0; col < COLS; col++) {
            pieces[1][col] = new Pawn(1, col); // Black pawns
            pieces[6][col] = new Pawn(6, col); // White pawns
        }
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        int cellSize = getWidth() / COLS;

        for (int row = 0; row < ROWS; row++) {
            for (int col = 0; col < COLS; col++) {
                Color color = (row + col) % 2 == 0 ? Color.WHITE : Color.GRAY;
                g.setColor(color);
                g.fillRect(col * cellSize, row * cellSize, cellSize, cellSize);

                ChessPiece piece = pieces[row][col];
                if (piece != null) {
                    piece.setBounds(col * cellSize, row * cellSize, cellSize, cellSize);
                    add(piece);
                }
            }
        }
    }
}