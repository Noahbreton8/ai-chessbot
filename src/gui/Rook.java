package gui;

import java.awt.*;

public class Rook extends ChessPiece {
    public Rook(int row, int col) {
        super(row, col, "\\images\\R.png"); // Adjust the image path based on your file structure
    }
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        // Drawing for the rook
        g.setColor(Color.BLACK);
        g.fillRect(10, 10, getWidth() - 20, getHeight() - 20);
    }

    // Add specific logic for rook movement if needed
}