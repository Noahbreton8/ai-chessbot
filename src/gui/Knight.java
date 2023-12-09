package gui;

import java.awt.*;

public class Knight extends ChessPiece {
    public Knight(int row, int col) {
        super(row, col, "\\images\\N.png"); // Adjust the image path based on your file structure
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        // Drawing for the knight
        g.setColor(Color.BLACK);
        g.fillOval(10, 10, getWidth() - 20, getHeight() - 20);
    }

    // Add specific logic for knight movement if needed
}