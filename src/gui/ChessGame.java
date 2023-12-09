package gui;
import javax.swing.*;

public class ChessGame {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("Chess Game");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setSize(800, 800);

            ChessBoardPanel chessBoard = new ChessBoardPanel();
            frame.add(chessBoard);

            frame.setVisible(true);
        });
    }
}