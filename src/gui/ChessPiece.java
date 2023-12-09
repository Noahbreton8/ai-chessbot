package gui;

import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.net.URL;
import java.io.IOException;
import javax.imageio.ImageIO;

public abstract class ChessPiece extends JButton {
    private int row;
    private int col;
    private BufferedImage image;

    public ChessPiece(int row, int col, String imagePath) {
        this.row = row;
        this.col = col;

        try {

            System.out.println("Working Directory: " + System.getProperty("user.dir"));

            // Use ClassLoader.getResource to load the image
            URL imageURL = getClass().getClassLoader().getResource("src\\imagePath");

            if (imageURL != null) {
                image = ImageIO.read(imageURL);
            } else {
                throw new IOException("Image not found: " + imagePath);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        setPreferredSize(new Dimension(image.getWidth(), image.getHeight()));
    }

    public int getRow() {
        return row;
    }

    public int getCol() {
        return col;
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        // Draw the image for the chess piece
        if (image != null) {
            g.drawImage(image, 0, 0, getWidth(), getHeight(), this);
        }
    }
}