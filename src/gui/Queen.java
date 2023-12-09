package gui;

import java.awt.*;

public class Queen extends ChessPiece {
    public Queen(int row, int col) {
        super(row, col, "\\images\\Q.png"); // Adjust the image path based on your file structure
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        // Drawing for the queen
        g.setColor(Color.BLACK);
        g.fillRect(10, 10, getWidth() - 20, getHeight() - 20);
        g.drawLine(10, 10, getWidth() - 10, getHeight() - 10);
        g.drawLine(10, getHeight() - 10, getWidth() - 10, 10);
    }

    // Add specific logic for queen movement if needed
}