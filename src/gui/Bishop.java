package gui;

import java.awt.*;

public class Bishop extends ChessPiece {
    public Bishop(int row, int col) {
        super(row, col, "\\images\\B.png"); // Adjust the image path based on your file structure
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        // Drawing for the bishop
        g.setColor(Color.BLACK);
        g.drawLine(10, 10, getWidth() - 10, getHeight() - 10);
        g.drawLine(10, getHeight() - 10, getWidth() - 10, 10);
    }

    // Add specific logic for bishop movement if needed
}