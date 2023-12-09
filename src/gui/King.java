package gui;

import java.awt.*;

public class King extends ChessPiece {
    public King(int row, int col) {
        super(row, col, "\\images\\K.png"); // Adjust the image path based on your file structure
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        // Drawing for the king
        g.setColor(Color.BLACK);
        g.fillRect(10, 10, getWidth() - 20, getHeight() - 20);
        g.drawLine(10, 10, getWidth() - 10, getHeight() - 10);
        g.drawLine(10, getHeight() - 10, getWidth() - 10, 10);
    }

    // Add specific logic for king movement if needed
}