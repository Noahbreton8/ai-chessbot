package gui;
import java.awt.*;

public class Pawn extends ChessPiece {
    public Pawn(int row, int col) {
        super(row, col, "\\images\\P.png"); // Adjust the image path based on your file structure
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        // Drawing for the pawn
        g.setColor(Color.BLACK);
        g.fillOval(10, 10, getWidth() - 20, getHeight() - 20);
    }

    // Add specific logic for pawn movement if needed
}